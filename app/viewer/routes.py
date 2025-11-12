from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Graph, Dataset, User
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app import db
from sqlalchemy import or_

viewer = Blueprint('viewer', __name__, template_folder='templates')

@viewer.route('/viewer/dashboard')
@login_required
def viewer_dashboard():
    """Viewer dashboard - Overview and quick stats"""
    
    # Quick stats
    total_graphs = Graph.query.count()
    total_datasets = Dataset.query.count()
    
    # Analysis type distribution
    analysis_types = db.session.query(
        Graph.analysis_type, 
        func.count(Graph.id).label('count')
    ).group_by(Graph.analysis_type).all()
    
    # Recent graphs (last 10)
    recent_graphs = Graph.query.order_by(Graph.created_at.desc()).limit(10).all()
    
    # Most popular graph types
    popular_types = db.session.query(
        Graph.graph_type,
        func.count(Graph.id).label('count')
    ).group_by(Graph.graph_type).order_by(desc('count')).limit(5).all()
    
    # Weekly activity
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_activity = Graph.query.filter(
        Graph.created_at >= week_ago
    ).count()

    return render_template('viewer_dashboard.html',
        total_graphs=total_graphs,
        total_datasets=total_datasets,
        analysis_types=analysis_types,
        recent_graphs=recent_graphs,
        popular_types=popular_types,
        weekly_activity=weekly_activity
    )

@viewer.route('/viewer/search')
@login_required
def search():
    """Search graphs with filters"""
    
    # Get filter parameters
    search_term = request.args.get('search', '').strip()
    analysis_type = request.args.get('analysis_type', '')
    graph_type = request.args.get('graph_type', '')
    dataset_id = request.args.get('dataset_id', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Base query
    graphs_query = Graph.query.join(User).join(Dataset)
    
    # Apply filters
    if search_term:
        graphs_query = graphs_query.filter(
            or_(
                Graph.name.ilike(f'%{search_term}%'),
                Dataset.filename.ilike(f'%{search_term}%')
            )
        )
    
    if analysis_type:
        graphs_query = graphs_query.filter(Graph.analysis_type == analysis_type)
    
    if graph_type:
        graphs_query = graphs_query.filter(Graph.graph_type == graph_type)
    
    if dataset_id:
        graphs_query = graphs_query.filter(Graph.dataset_id == dataset_id)
    
    if date_from:
        graphs_query = graphs_query.filter(Graph.created_at >= date_from)
    
    if date_to:
        graphs_query = graphs_query.filter(Graph.created_at <= date_to)
    
    graphs = graphs_query.order_by(Graph.created_at.desc()).all()
    
    # Get filter options
    datasets = Dataset.query.all()
    analysis_types = db.session.query(Graph.analysis_type).distinct().all()
    graph_types = db.session.query(Graph.graph_type).distinct().all()
    
    return render_template(
        'search.html',
        graphs=graphs,
        datasets=datasets,
        analysis_types=[at[0] for at in analysis_types],
        graph_types=[gt[0] for gt in graph_types],
        search_term=search_term,
        selected_analysis_type=analysis_type,
        selected_graph_type=graph_type,
        selected_dataset=dataset_id,
        date_from=date_from,
        date_to=date_to
    )

@viewer.route('/viewer/insights')
@login_required
def insights():
    """Viewer Insights Center — trends, recommendations, usage patterns"""

    # Most viewed graphs
    most_viewed = Graph.query.order_by(Graph.view_count.desc()).limit(5).all() \
        if hasattr(Graph, 'view_count') else []

    # Trending analysis types
    trending_analysis = db.session.query(
        Graph.analysis_type, func.count(Graph.id).label('count')
    ).group_by(Graph.analysis_type).order_by(desc('count')).limit(5).all()

    # Analyst leaderboard (top creators)
    analyst_rank = db.session.query(
        User.name, func.count(Graph.id).label('count')
    ).join(Graph, Graph.created_by == User.id)\
     .group_by(User.id).order_by(desc('count')).limit(5).all()

    # Weekly activity — number of graphs created in last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_graphs = Graph.query.filter(Graph.created_at >= week_ago).count()

    # Recommendations (simple version: latest graphs not viewed by user)
    recommended_graphs = Graph.query.order_by(Graph.created_at.desc()).limit(6).all()

    return render_template(
        'viewer_insights.html',
        most_viewed=most_viewed,
        trending_analysis=trending_analysis,
        analyst_rank=analyst_rank,
        weekly_graphs=weekly_graphs,
        recommended_graphs=recommended_graphs
    )
