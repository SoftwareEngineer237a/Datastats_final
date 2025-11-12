import os
import pandas as pd
import numpy as np
from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file, current_app, Response
from werkzeug.utils import secure_filename
from app.forms import DatasetUploadForm, CleanTransformForm
from flask_login import login_required, current_user
from app.models import Dataset, AnalysisLog, Graph
from datetime import datetime, timezone
from app.analyst import *
from app import db
from app.utils import load_dataset_by_id, save_cleaned_dataframe  # custom utility functions
from analysis_engine.cleaning import clean_and_transform_data  # custom module you'll define
from analysis_engine.statistics import compute_descriptive_stats  # to be defined
from analysis_engine.statistics import calculate_confidence_interval, one_sample_ttest
from analysis_engine.dimensionality import run_pca, run_mca
from analysis_engine.density_curve import run_density_curve
from analysis_engine.visualization import render_chart
from app.models import Report
import uuid
from analysis_engine.matrix_tools import compute_correlation, compute_covariance
from analysis_engine.time_series import (
    prepare_series,
    moving_average,
    run_exponential_smoothing,
    run_arima,
    run_seasonal_decomposition,
    run_trend_analysis
)

analyst = Blueprint('analyst', __name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@analyst.route('/analyst/dashboard')
@login_required
def dashboard():
    # Basic stats
    total_datasets = Dataset.query.filter_by(user_id=current_user.id).count()
    total_analyses = AnalysisLog.query.filter_by(user_id=current_user.id).count()
    
    recent_upload = Dataset.query.filter_by(user_id=current_user.id).order_by(Dataset.uploaded_on.desc()).first()
    recent_upload_date = recent_upload.uploaded_on.strftime("%Y-%m-%d") if recent_upload else "N/A"
    
    completed_reports = AnalysisLog.query.filter_by(user_id=current_user.id, status='completed').count()
    pending_reports = AnalysisLog.query.filter_by(user_id=current_user.id, status='pending').count()

    # Recent uploaded datasets (last 5)
    recent_uploads = Dataset.query.filter_by(user_id=current_user.id).order_by(Dataset.uploaded_on.desc()).limit(5).all()

    # Recent activity logs (last 5)
    activity_logs = AnalysisLog.query.filter_by(user_id=current_user.id).order_by(AnalysisLog.timestamp.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        stats={
            'total_datasets': total_datasets,
            'total_analyses': total_analyses,
            'recent_upload': recent_upload_date,
            'completed_reports': completed_reports,
            'pending_reports': pending_reports
        },
        recent_uploads=recent_uploads,
        activity_logs=activity_logs
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analyst.route('/analyst/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = DatasetUploadForm()
    table_html = None
    dataset_id = None

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        if allowed_file(filename):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                elif filename.endswith('.xlsx'):
                    df = pd.read_excel(filepath)
                elif filename.endswith('.json'):
                    df = pd.read_json(filepath)
                else:
                    flash('Unsupported file format', 'danger')
                    return redirect(url_for('analyst.upload'))

                table_html = df.head(50).to_html(classes='data-table table table-striped', index=False)
                flash('File uploaded and previewed successfully.', 'success')

                dataset = Dataset(filename=filename, user_id=current_user.id)
                db.session.add(dataset)
                db.session.commit()
                dataset_id = dataset.id 

            except Exception as e:
                flash(f'Error reading file: {e}', 'danger')
        else:
            flash('Invalid file type. Only CSV, Excel, and JSON are allowed.', 'danger')

    return render_template('upload.html', 
                           form=form, 
                           table_html=table_html,
                           dataset_id=dataset_id)


@analyst.route('/dataset/<int:dataset_id>/clean', methods=['GET', 'POST'])
@login_required
def clean_data(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    form = CleanTransformForm()
    
    if not dataset_path:
        flash("Dataset not found", "danger")
        return redirect(url_for('analyst.upload'))

    # Load dataset
    try:
        if dataset_path.endswith('.csv'):
            df = pd.read_csv(dataset_path)
        else:
            df = pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    if request.method == 'POST':
        try:
            cleaned_df = clean_and_transform_data(df.copy(), request.form)
            cleaned_df_html = cleaned_df.to_html(classes='table table-bordered table-striped', index=False)

            return render_template(
                'clean_transform.html',
                df=cleaned_df,
                df_html=cleaned_df_html,
                dataset_id=dataset_id,
                form=form
            )
        except Exception as e:
            flash(f"Error cleaning data: {e}", "danger")

    # GET request
    df_html = df.to_html(classes='table table-bordered table-striped', index=False)
    return render_template(
        'clean_transform.html',
        df=df,
        df_html=df_html,
        dataset_id=dataset_id,
        form=form
    )

# ─── DESCRIPTIVE STATISTICS ─────────────────────────────

@analyst.route('/dataset/<int:dataset_id>/describe', methods=['GET'])
@login_required
def describe_dataset(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found", "danger")
        return redirect(url_for('analyst.upload'))

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
        output_dir = os.path.join("app", "static", "results")
        desc_stats, csv_file = compute_descriptive_stats(
            df,
            output_dir=output_dir,
            filename_prefix=f"desc_stats_{dataset_id}"
        )
    except Exception as e:
        flash(f"Error processing dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    return render_template('descriptive_stats.html',
                           df=df,
                           stats_table=desc_stats.to_html(classes="table table-bordered table-striped", index=True),
                           dataset_id=dataset_id,
                           csv_file=csv_file)

@analyst.route('/dataset/<int:dataset_id>/inferential', methods=['GET', 'POST'])
@login_required
def inferential_stats(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    results = {}

    if request.method == 'POST':
        column = request.form.get('column')
        popmean = float(request.form.get('popmean', 0))
        confidence = float(request.form.get('confidence', 0.95))

        if column and column in numeric_cols:
            data = df[column].dropna()
            results['ci'] = calculate_confidence_interval(data, confidence)
            results['ttest'] = one_sample_ttest(data, popmean)
            results['selected_column'] = column

    return render_template('inferential_stats.html',
                           dataset_id=dataset_id,
                           numeric_cols=numeric_cols,
                           results=results)

@analyst.route('/dataset/<int:dataset_id>/regression', methods=['GET', 'POST'])
@login_required
def regression_analysis(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    result = None
    model_type = None

    if request.method == 'POST':
        x_col = request.form.get('x_column')
        y_cols = request.form.getlist('y_column')  # list for multiple Ys
        model_type = request.form.get('model_type')
        degree = int(request.form.get('degree', 2))

        if x_col and y_cols and model_type:
            try:
                from analysis_engine.regression import run_regression
                output_dir = os.path.join("app", "static", "results")
                result = run_regression(
                    df, x_col, y_cols, model_type, degree,
                    output_dir=output_dir,
                    prefix=f"regression_{dataset_id}"
                )

            except ValueError as e:
                flash(str(e), 'danger')
            except Exception as e:
                flash(f"Regression error: {e}", 'danger')

    return render_template('regression_analysis.html',
                           dataset_id=dataset_id,
                           numeric_cols=numeric_cols,
                           result=result,
                           model_type=model_type,
                           csv_file=result.get("csv") if result else None
                           )

@analyst.route('/dataset/<int:dataset_id>/ml', methods=['GET', 'POST'])
@login_required
def machine_learning_analysis(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_cols = df.columns.tolist()

    result = None

    if request.method == 'POST':
        x_col = request.form.get('x_column')
        y_col = request.form.get('y_column')
        model_type = request.form.get('model_type')
        task_type = request.form.get('task_type')
        n_neighbors = int(request.form.get('n_neighbors', 3))

        output_dir = os.path.join('app', 'static', 'results')
        filename_prefix = f"ml_{dataset_id}"

        try:
            from analysis_engine.machine_learning import run_ml_model
            result = run_ml_model(df, x_col, y_col, model_type, task_type, n_neighbors, output_dir, filename_prefix)
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('ml_models.html',
                           dataset_id=dataset_id,
                           numeric_cols=numeric_cols,
                           all_cols=all_cols,
                           result=result,
                           csv_file=result.get("csv") if result else None)


@analyst.route('/dataset/<int:dataset_id>/dimensionality', methods=['GET', 'POST'])
@login_required
def dimensionality_analysis(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    dataset = Dataset.query.get_or_404(dataset_id)

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    result = None
    method = None

    if request.method == 'POST':
        try:
            method = request.form.get('method')
            selected_cols = request.form.getlist('columns')

            output_dir = os.path.join(current_app.root_path, 'static', 'generated')
            os.makedirs(output_dir, exist_ok=True)

            if method == 'PCA' and selected_cols:
                custom_ratios = {
                    "Subvention_to_Income": ("subvs", "pib2022"),
                    "Revenue_to_Salary": ("revenue", "salary")
                }
                result = run_pca(df, selected_cols, output_dir, custom_ratios)
                
                # Save PCA graphs to database
                if result:
                    graphs_to_save = [
                        ('scree_plot', 'Scree Plot'),
                        ('biplot', 'PCA Biplot'),
                        ('correlation_circle', 'Correlation Circle')
                    ]
                    
                    for key, name in graphs_to_save:
                        if result.get(key):
                            file_path = os.path.join('generated', result[key])
                            new_graph = Graph(
                                name=f"PCA - {name}",
                                graph_type='PCA',
                                dataset_id=dataset_id,
                                analysis_type='dimensionality',
                                file_path=file_path,
                                created_by=current_user.id
                            )
                            db.session.add(new_graph)
                    
                    db.session.commit()
                    flash("PCA analysis saved successfully!", "success")

            elif method == 'MCA' and selected_cols:
                result = run_mca(df, selected_cols, output_dir)
                
                # Save MCA graph to database
                if result and result.get('mca_map') and not result.get('error'):
                    file_path = os.path.join('generated', result['mca_map'])
                    new_graph = Graph(
                        name=f"MCA - Factorial Map",
                        graph_type='MCA',
                        dataset_id=dataset_id,
                        analysis_type='dimensionality',
                        file_path=file_path,
                        created_by=current_user.id
                    )
                    db.session.add(new_graph)
                    db.session.commit()
                    flash("MCA analysis saved successfully!", "success")

            else:
                flash("Please select a method and at least one column.", "danger")

        except Exception as e:
            flash(f"Error during analysis: {e}", "danger")
            db.session.rollback()

    # Fetch dimensionality graphs from database
    graphs = Graph.query.filter_by(
        dataset_id=dataset_id,
        analysis_type='dimensionality'
    ).order_by(Graph.created_at.desc()).all()

    return render_template(
        'dimensionality.html',
        dataset_id=dataset_id,
        dataset_name=dataset.filename,
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        all_cols=df.columns.tolist(),
        result=result,
        method=method,
        graphs=graphs)

@analyst.route('/dataset/<int:dataset_id>/clustering', methods=['GET', 'POST'])
@login_required
def clustering(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    result = {}

    if request.method == 'POST':
        selected_cols = request.form.getlist('columns')
        algorithm = request.form.get('algorithm')
        n_clusters = int(request.form.get('n_clusters', 3))
        method = request.form.get('hac_method', 'ward')

        output_dir = os.path.join('app', 'static', 'img')
        os.makedirs(output_dir, exist_ok=True)

        try:
            from analysis_engine.clustering import run_kmeans, run_hac

            if algorithm == 'kmeans':
                result = run_kmeans(df, selected_cols, n_clusters, output_dir)
                graph_name = f"K-Means Clustering (k={n_clusters})"
                plot_key = 'kmeans_plot'
            elif algorithm == 'hac':
                result = run_hac(df, selected_cols, output_dir, method=method)
                graph_name = f"HAC Dendrogram ({method})"
                plot_key = 'hac_plot'
            
            # Save to database
            if result and result.get(plot_key):
                file_path = os.path.join('img', result[plot_key])
                
                new_graph = Graph(
                    name=graph_name,
                    graph_type=algorithm,
                    dataset_id=dataset_id,
                    analysis_type='clustering',
                    file_path=file_path,
                    created_by=current_user.id
                )
                db.session.add(new_graph)
                db.session.commit()
                
                flash(f"Clustering analysis '{graph_name}' saved successfully!", "success")
                
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            db.session.rollback()

    # Fetch clustering graphs from database
    graphs = Graph.query.filter_by(
        dataset_id=dataset_id,
        analysis_type='clustering'
    ).order_by(Graph.created_at.desc()).all()

    return render_template('clustering.html',
                           dataset_id=dataset_id,
                           numeric_cols=numeric_cols,
                           result=result,
                           graphs=graphs)

@analyst.route('/dataset/<int:dataset_id>/timeseries', methods=['GET', 'POST'])
@login_required
def time_series_analysis(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    date_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.datetime64) or df[c].dtype == 'object']
    num_cols = df.select_dtypes(include='number').columns.tolist()

    result = None
    method = None

    if request.method == 'POST':
        method = request.form.get('method')
        date_col = request.form.get('date_col')
        value_col = request.form.get('value_col')
        freq = request.form.get('freq') or None
        agg = request.form.get('agg') or 'mean'
        output_dir = os.path.join('app', 'static', 'img')
        os.makedirs(output_dir, exist_ok=True)

        if not date_col or not value_col:
            flash("Please select both date and value columns.", "danger")
            return render_template('time_series.html',
                                   dataset_id=dataset_id,
                                   date_cols=df.columns.tolist(),
                                   num_cols=num_cols,
                                   result=None,
                                   method=method)

        try:
            series = prepare_series(df, date_col, value_col, freq=freq, agg=agg)
        except Exception as e:
            flash(f"Error preparing series: {e}", "danger")
            return render_template('time_series.html',
                                   dataset_id=dataset_id,
                                   date_cols=df.columns.tolist(),
                                   num_cols=num_cols,
                                   result=None,
                                   method=method)

        name_prefix = f"ts_{dataset_id}_{method}_{value_col}"

        try:
            if method == 'moving_average':
                window = int(request.form.get('ma_window', 3))
                result = moving_average(series, window=window, output_dir=output_dir, name_prefix=name_prefix)
                graph_name = f"Moving Average - {value_col} (window={window})"

            elif method == 'exp_smoothing':
                trend = request.form.get('trend', 'add')
                seasonal = request.form.get('seasonal', 'none')
                seasonal_periods = request.form.get('seasonal_periods', '')
                seasonal_periods = int(seasonal_periods) if seasonal_periods else None
                result = run_exponential_smoothing(series, trend=trend, seasonal=seasonal,
                                                   seasonal_periods=seasonal_periods,
                                                   output_dir=output_dir, name_prefix=name_prefix)
                graph_name = f"Exponential Smoothing - {value_col}"

            elif method == 'arima':
                p = int(request.form.get('arima_p', 1))
                d = int(request.form.get('arima_d', 1))
                q = int(request.form.get('arima_q', 1))
                steps = int(request.form.get('forecast_steps', 12))
                result = run_arima(series, order=(p, d, q), forecast_steps=steps,
                                   output_dir=output_dir, name_prefix=name_prefix)
                graph_name = f"ARIMA({p},{d},{q}) - {value_col}"

            elif method == 'decomposition':
                model = request.form.get('decomp_model', 'additive')
                period = int(request.form.get('decomp_period', 12))
                result = run_seasonal_decomposition(series, model=model, period=period,
                                                    output_dir=output_dir, name_prefix=name_prefix)
                graph_name = f"Seasonal Decomposition - {value_col}"

            elif method == 'trend':
                result = run_trend_analysis(series, output_dir=output_dir, name_prefix=name_prefix)
                graph_name = f"Trend Analysis - {value_col}"

            else:
                flash("Unknown method.", "danger")
                
            # Save to database
            if result and result.get('plot'):
                file_path = os.path.join('img', result['plot'])
                
                new_graph = Graph(
                    name=graph_name,
                    graph_type=method,
                    dataset_id=dataset_id,
                    analysis_type='time_series',
                    file_path=file_path,
                    created_by=current_user.id
                )
                db.session.add(new_graph)
                db.session.commit()
                
                flash(f"Time series analysis '{graph_name}' saved successfully!", "success")

        except Exception as e:
            flash(f"Analysis error: {e}", "danger")
            db.session.rollback()

    # Fetch time series graphs from database
    graphs = Graph.query.filter_by(
        dataset_id=dataset_id,
        analysis_type='time_series'
    ).order_by(Graph.created_at.desc()).all()

    return render_template('time_series.html',
                           dataset_id=dataset_id,
                           date_cols=df.columns.tolist(),
                           num_cols=num_cols,
                           result=result,
                           method=method,
                           graphs=graphs)

@analyst.route('/dataset/<int:dataset_id>/matrix', methods=['GET', 'POST'])
@login_required
def matrix_operations(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    # Load uploaded data
    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    # Numeric columns only
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    result = None
    method = None

    if request.method == 'POST':
        method = request.form.get('method')
        selected_cols = request.form.getlist('columns')

        if not selected_cols or len(selected_cols) < 2:
            flash("Select at least two numeric columns.", "warning")
            return render_template('matrix_ops.html',
                                   dataset_id=dataset_id,
                                   numeric_cols=numeric_cols,
                                   result=None,
                                   method=method,
                                   graphs=None)

        output_dir = os.path.join('app', 'static', 'img')
        os.makedirs(output_dir, exist_ok=True)
        prefix = f"matrix_{dataset_id}"

        try:
            if method == 'correlation':
                corr_method = request.form.get('corr_method', 'pearson')
                na_policy = request.form.get('na_policy', 'pairwise')
                result = compute_correlation(
                    df, selected_cols, method=corr_method,
                    handle_na=na_policy, output_dir=output_dir,
                    name_prefix=prefix
                )
                
                # Save correlation matrix to database
                if result and result.get('heatmap'):
                    file_path = os.path.join('img', result['heatmap'])
                    graph_name = f"Correlation Matrix ({corr_method.capitalize()})"
                    
                    new_graph = Graph(
                        name=graph_name,
                        graph_type='correlation',
                        dataset_id=dataset_id,
                        analysis_type='matrix',
                        file_path=file_path,
                        created_by=current_user.id
                    )
                    db.session.add(new_graph)
                    db.session.commit()
                    
                    flash(f"Correlation matrix '{graph_name}' saved successfully!", "success")
                    
            elif method == 'covariance':
                ddof = int(request.form.get('ddof', 1))
                na_policy = request.form.get('na_policy', 'complete')
                result = compute_covariance(
                    df, selected_cols, ddof=ddof,
                    handle_na=na_policy, output_dir=output_dir,
                    name_prefix=prefix
                )
                
                # Save covariance matrix to database
                if result and result.get('heatmap'):
                    file_path = os.path.join('img', result['heatmap'])
                    graph_name = f"Covariance Matrix (ddof={ddof})"
                    
                    new_graph = Graph(
                        name=graph_name,
                        graph_type='covariance',
                        dataset_id=dataset_id,
                        analysis_type='matrix',
                        file_path=file_path,
                        created_by=current_user.id
                    )
                    db.session.add(new_graph)
                    db.session.commit()
                    
                    flash(f"Covariance matrix '{graph_name}' saved successfully!", "success")
            else:
                flash("Unknown method selected.", "danger")
                
        except Exception as e:
            flash(f"Computation error: {e}", "danger")
            db.session.rollback()

    # Fetch matrix graphs from database
    graphs = Graph.query.filter_by(
        dataset_id=dataset_id,
        analysis_type='matrix'
    ).order_by(Graph.created_at.desc()).all()

    return render_template('matrix_ops.html',
                           dataset_id=dataset_id,
                           numeric_cols=numeric_cols,
                           method=method,
                           result=result,
                           graphs=graphs)

@analyst.route('/dataset/<int:dataset_id>/density-curve', methods=['GET', 'POST'])
@login_required
def density_curve(dataset_id):
    """Generate and display density curve"""
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    # Load dataset
    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    result = None

    if request.method == 'POST':
        column = request.form.get('column')
        color = request.form.get('color', 'green')  # default green

        if not column:
            flash("Please select a column.", "warning")
        else:
            try:
                result = run_density_curve(df, column, color, dataset_id, current_user.id)
                flash(f"Density curve for '{column}' generated successfully!", "success")
            except Exception as e:
                flash(f"Error generating curve: {e}", "danger")

    return render_template(
        'density_curve.html',
        dataset_id=dataset_id,
        numeric_cols=numeric_cols,
        result=result
    )

@analyst.route('/dataset/<int:dataset_id>/visualize', methods=['GET', 'POST'])
@login_required
def visualizations(dataset_id):
    dataset_path = load_dataset_by_id(dataset_id)
    if not dataset_path:
        flash("Dataset not found.", "danger")
        return redirect(url_for('analyst.upload'))

    # Load dataframe
    try:
        df = pd.read_csv(dataset_path) if dataset_path.endswith('.csv') else pd.read_excel(dataset_path)
    except Exception as e:
        flash(f"Error loading dataset: {e}", "danger")
        return redirect(url_for('analyst.upload'))

    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = [c for c in all_cols if c not in num_cols]

    result = None
    chart_type = request.form.get('chart_type') if request.method == 'POST' else None
    subtype = request.form.get('subtype') if request.method == 'POST' else None

    if request.method == 'POST':
        cfg = {
            "chart_type": chart_type,
            "subtype": subtype,
            "interactive": request.form.get('interactive'),

            # generic fields
            "x": request.form.get('x'),
            "y": request.form.get('y'),
            "y2": request.form.get('y2'),
            "z": request.form.get('z'),
            "group": request.form.get('group'),
            "size": request.form.get('size'),
            "color": request.form.get('color'),
            "bins": request.form.get('bins', ''),
            "agg": request.form.get('agg'),
            "stacked": request.form.get('stacked'),
            "orientation": request.form.get('orientation'),
            "donut": request.form.get('donut'),
            "explode": request.form.get('explode'),
            "parent": request.form.get('parent'),

            # network / sankey
            "source_col": request.form.get('source_col'),
            "target_col": request.form.get('target_col'),
            "value_col": request.form.get('value_col'),
            "weight_col": request.form.get('weight_col'),
            "corr_threshold": request.form.get('corr_threshold', 0.6),

            # gantt
            "start_col": request.form.get('start_col'),
            "end_col": request.form.get('end_col'),

            # map
            "geo_col": request.form.get('geo_col'),
            "geo_mode": request.form.get('geo_mode'),
            "lat_col": request.form.get('lat_col'),
            "lon_col": request.form.get('lon_col'),

            # dendrogram
            "standardize": request.form.get('standardize'),
            "linkage_method": request.form.get('linkage_method', 'ward'),
        }

        # multi-selects
        y_multi = request.form.getlist('y_multi')
        if y_multi:
            cfg["y_multi"] = y_multi

        # Convert bins to int if provided
        if cfg.get("bins"):
            try:
                cfg["bins"] = int(cfg["bins"])
            except Exception:
                cfg["bins"] = 10

        try:
            output_img_dir = os.path.join('app', 'static', 'img')
            output_html_dir = os.path.join('app', 'static', 'html')
            os.makedirs(output_img_dir, exist_ok=True)
            os.makedirs(output_html_dir, exist_ok=True)

            prefix = f"viz_{dataset_id}"
            result = render_chart(df, cfg, output_img_dir, output_html_dir, prefix,
                                  dataset_id=dataset_id, user_id=current_user.id)
            
            # Save graph to database after successful creation
            if result and result.get('image_path'):
                # Determine graph name
                graph_name = f"{chart_type}"
                if subtype:
                    graph_name += f" - {subtype}"
                if cfg.get('x'):
                    graph_name += f" ({cfg['x']}"
                    if cfg.get('y'):
                        graph_name += f" vs {cfg['y']}"
                    graph_name += ")"
                
                # Create Graph record
                new_graph = Graph(
                    name=graph_name,
                    graph_type=chart_type,
                    dataset_id=dataset_id,
                    analysis_type='visualization',
                    file_path=result['image_path'],  # Store relative path
                    created_by=current_user.id
                )
                db.session.add(new_graph)
                db.session.commit()
                
                flash(f"Visualization '{graph_name}' saved successfully!", "success")
                
        except Exception as e:
            flash(f"Visualization error: {e}", "danger")
            db.session.rollback()

    # Fetch all graphs for this dataset from database
    graphs = Graph.query.filter_by(
        dataset_id=dataset_id,
        analysis_type='visualization'
    ).order_by(Graph.created_at.desc()).all()

    # Generate df_html for template
    df_html = df.head(10).to_html(classes='table table-striped table-bordered', index=False)

    return render_template('visualizations.html',
                           dataset_id=dataset_id,
                           all_cols=all_cols, 
                           num_cols=num_cols, 
                           cat_cols=cat_cols,
                           result=result, 
                           chart_type=chart_type, 
                           subtype=subtype,
                           df_html=df_html,
                           graphs=graphs)


@analyst.route('/download_graph/<int:graph_id>')
@login_required
def download_graph(graph_id):
    graph = Graph.query.get_or_404(graph_id)
    file_path = os.path.join(current_app.root_path, 'static', graph.file_path)
    
    if not os.path.exists(file_path):
        flash("Fichier introuvable.", "danger")
        return redirect(request.referrer or url_for('analyst.history'))
    
    def generate():
        with open(file_path, 'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    
    # Get filename and extension
    filename = os.path.basename(file_path)
    if not filename:
        filename = f"{graph.name}.png"
    
    return Response(
        generate(),
        mimetype='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'application/octet-stream'
        }
    )


@analyst.route('/history')
@login_required
def history():
    from app.models import Graph  # if not already imported
    graphs = Graph.query.filter_by(created_by=current_user.id).order_by(Graph.created_at.desc()).all()
    return render_template('history.html', graphs=graphs)


@analyst.route('/dataset/<int:dataset_id>/chatbox', methods=['GET'])
@login_required
def chatbox(dataset_id):
    # You can pass additional context if needed
    return render_template('chatbox.html', dataset_id=dataset_id, current_dataset_id=dataset_id)