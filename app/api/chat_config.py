# app/api/chat_config.py
"""
Configuration constants used by the chat API and local domain handler.

This file defines simple keyword maps and canned answers for Datastats-specific
questions so the chatbot can answer precisely about the application without
always calling an external model.
"""

# Keywords that the DomainValidator will look for when doing a quick check.
# Each key maps to a list of lowercase keywords/phrases that indicate the
# user's question belongs to that domain.
ALLOWED_KEYWORDS = {
    "datastats_app": [
        "datastats",
        "what is datastats",
        "what does datastats do",
        "cnef",
        "central bank",
        "bank",
        "microfinance",
        "data analysis app",
    ],
}

# Canned restriction message returned when a question is outside allowed domains
RESTRICTION_MESSAGE = (
    "Sorry — I can't help with that request. This assistant only answers "
    "questions about permitted data-analysis domains and the Datastats app."
)

# Small system context used when calling the LLM (kept short here; can be
# expanded). The domain handler will answer app-specific questions locally
# before deferring to the model.
ENHANCED_SYSTEM_CONTEXT = (
    "You are an assistant for Datastats, an internal data-analysis app built by "
    "the national economic and financial committee (CNEF) for the central bank. "
    "Answer questions about the app, its purpose, features, and analysis types."
)

# Prompt used by the fallback external classifier (if used). Keep it concise.
CLASSIFICATION_PROMPT = (
    "Classify whether the following user message is about the Datastats app "
    "or not. Reply with 'ALLOWED' or 'DENIED'."
)

# Local knowledge base: canned answers keyed by domain. These are authoritative
# answers used to respond immediately to questions about the app.
APP_ANSWERS = {
    "datastats_app": (
        "Datastats is an internal data-analysis application developed at the "
        "national economic and financial committee (CNEF) by experts and academic "
        "interns for use by the central bank. It supports economic and financial "
        "simulations and data processing for banking and microfinance datasets. "
        "The goal is to provide the central bank with an in-house analytical tool "
        "so teams don't have to depend on external software like Excel, Stata, R, "
        "Shiny, Jupyter, or Power BI. Datastats includes features for data cleaning, "
        "descriptive and inferential statistics, regressions, clustering, time-series "
        "analysis, visualizations, and export capabilities for reports and CSV/PDF."
    )
}

ALLOWED_KEYWORDS = {
    'greetings': [
        # English greetings
        'hello', 'hi', 'hey', 'yo', 'sup', 'what\'s up', 'howdy', 'greetings',
        'good morning', 'good afternoon', 'good evening', 'good night',
        'how are you', 'how do you do', 'nice to meet you', 'pleased to meet you',
        'thanks', 'thank you', 'much obliged', 'appreciate it', 'cheers',
        'goodbye', 'bye', 'see you', 'catch you later', 'farewell', 'adieu',
        'please', 'sorry', 'excuse me', 'pardon me', 'welcome', 'you\'re welcome',
        'no problem', 'my pleasure', 'anytime', 'sure thing',
        
        # French greetings
        'bonjour', 'bonsoir', 'salut', 'coucou', 'hello', 'allô',
        'comment allez-vous', 'comment ça va', 'ça va', 'quoi de neuf',
        'merci', 'merci beaucoup', 'de rien', 'je vous en prie',
        'au revoir', 'à bientôt', 'à plus tard', 'adieu', 'bonne nuit',
        's\'il vous plaît', 'pardon', 'excusez-moi', 'désolé', 'bienvenue',
        'enchanté', 'ravi de vous rencontrer', 'avec plaisir'
    ],

    'datastats_app': [
        # English - App specific terms
        'datastats', 'data stats', 'this app', 'this application', 'your app',
        'beac app', 'beac tool', 'beac platform', 'central bank app',
        'upload dataset', 'upload data', 'upload file', 'upload csv', 'upload excel',
        'data upload', 'file upload', 'import data', 'import dataset',
        'user roles', 'admin role', 'analyst role', 'viewer role', 'employee role',
        'login', 'logout', 'sign in', 'sign out', 'authentication', 'register',
        'dashboard', 'analyst dashboard', 'viewer dashboard', 'admin dashboard',
        'app features', 'app functionality', 'app capabilities', 'what can you do',
        'how to use', 'how does it work', 'tutorial', 'guide', 'help',
        'data cleaning', 'data transformation', 'data preprocessing',
        'missing values', 'outliers', 'data quality', 'data validation',
        'column selection', 'filter data', 'sort data', 'group data',
        'export results', 'download report', 'export pdf', 'export excel',
        'visualization dashboard', 'interactive plots', 'report generation',
        'audit logs', 'session management', 'access control', 'permissions',
        'file formats supported', 'csv files', 'excel files', 'json files',
        'data limits', 'file size', 'performance', 'speed',
        'internal tool', 'in-house tool', 'proprietary tool', 'custom solution',
        'bank data', 'microfinance data', 'financial institution data',
        'data processing', 'batch analysis', 'bulk analysis',
        'column types', 'numeric columns', 'text columns', 'date columns',
        'rename columns', 'merge columns', 'split columns',
        'currency conversion', 'unit conversion', 'date formatting',
        'template datasets', 'financial statements', 'predefined templates',
        
        # French - App specific terms
        'datastats', 'cette application', 'cette app', 'votre application',
        'application beac', 'outil beac', 'plateforme beac', 'app banque centrale',
        'télécharger données', 'télécharger fichier', 'télécharger csv', 'télécharger excel',
        'importation données', 'importer données', 'importer fichier',
        'rôles utilisateurs', 'rôle admin', 'rôle analyste', 'rôle visualiseur', 'rôle employé',
        'connexion', 'déconnexion', 'se connecter', 'authentification', 's\'inscrire',
        'tableau de bord', 'tableau de bord analyste', 'tableau de bord visualiseur',
        'fonctionnalités app', 'capacités app', 'que pouvez-vous faire',
        'comment utiliser', 'comment ça marche', 'tutoriel', 'guide', 'aide',
        'nettoyage données', 'transformation données', 'prétraitement données',
        'valeurs manquantes', 'valeurs aberrantes', 'qualité données', 'validation données',
        'sélection colonnes', 'filtrer données', 'trier données', 'grouper données',
        'exporter résultats', 'télécharger rapport', 'exporter pdf', 'exporter excel',
        'tableau de bord visualisation', 'graphiques interactifs', 'génération rapport',
        'journaux audit', 'gestion session', 'contrôle accès', 'permissions',
        'formats fichiers supportés', 'fichiers csv', 'fichiers excel', 'fichiers json',
        'limites données', 'taille fichier', 'performance', 'vitesse',
        'outil interne', 'outil maison', 'outil propriétaire', 'solution personnalisée',
        'données bancaires', 'données microfinance', 'données institutions financières',
        'traitement données', 'analyse par lot', 'analyse en masse',
        'types colonnes', 'colonnes numériques', 'colonnes texte', 'colonnes date',
        'renommer colonnes', 'fusionner colonnes', 'diviser colonnes',
        'conversion devise', 'conversion unités', 'formatage date',
        'modèles données', 'états financiers', 'modèles prédéfinis',
        'dépouillement', 'dépouillement de données', 'application de dépouillement'
    ],
    
    'finance': [
        # English finance terms
        'finance', 'financial', 'money', 'investment', 'portfolio', 'asset',
        'liability', 'equity', 'profit', 'loss', 'revenue', 'income', 'expense',
        'budget', 'cost', 'price', 'value', 'valuation', 'cash flow', 'roi',
        'return on investment', 'dividend', 'stock', 'bond', 'security',
        'capital', 'funding', 'venture capital', 'private equity', 'hedge fund',
        'mutual fund', 'etf', 'derivative', 'option', 'futures', 'commodity',
        'forex', 'currency', 'exchange', 'trading', 'broker', 'dealer',
        'market maker', 'liquidity', 'volatility', 'risk', 'diversification',
        'allocation', 'rebalancing', 'alpha', 'beta', 'sharpe ratio',
        'yield', 'coupon', 'maturity', 'duration', 'convexity', 'spread',
        'arbitrage', 'leverage', 'margin', 'collateral', 'syndication',
        'financial modeling', 'dcf', 'discounted cash flow', 'npv', 'net present value',
        'irr', 'internal rate of return', 'payback period', 'break-even',
        'financial statement', 'balance sheet', 'income statement', 'cash flow statement',
        'financial ratio', 'profitability ratio', 'liquidity ratio', 'solvency ratio',
        'efficiency ratio', 'leverage ratio', 'market ratio', 'valuation ratio',
        
        # French finance terms
        'finance', 'financier', 'argent', 'investissement', 'portefeuille', 'actif',
        'passif', 'capitaux propres', 'profit', 'perte', 'revenus', 'dépenses',
        'budget', 'coût', 'prix', 'valeur', 'évaluation', 'flux de trésorerie',
        'retour sur investissement', 'dividende', 'action', 'obligation', 'titre',
        'capital', 'financement', 'capital-risque', 'fonds propres',
        'bourse', 'marché', 'courtier', 'négociant', 'liquidité', 'volatilité',
        'risque', 'diversification', 'rendement', 'échéance', 'arbitrage',
        'modélisation financière', 'dcf', 'flux de trésorerie actualisés', 'npv', 'valeur actuelle nette',
        'tri', 'taux de rendement interne', 'période de récupération', 'seuil de rentabilité',
        'état financier', 'bilan', 'compte de résultat', 'tableau de flux de trésorerie',
        'ratio financier', 'ratio de rentabilité', 'ratio de liquidité', 'ratio de solvabilité',
        'ratio d\'efficacité', 'ratio d\'endettement', 'ratio de marché', 'ratio d\'évaluation'
            
        # Historical finance terms
        'tulip mania', 'south sea bubble', 'great depression', 'black monday',
        'dot com bubble', '2008 financial crisis', 'bretton woods',
        'gold standard', 'federal reserve act', 'glass-steagall act',
        'securities act', 'investment company act', 'sarbanes-oxley',
        'dodd-frank', 'basel accords', 'mifid', 'volcker rule',
        'history of finance', 'financial history', 'economic history',
        'banking history', 'wall street history', 'stock market crash'
    ],
    
    'banking': [
        # English banking terms
        'bank', 'banking', 'loan', 'credit', 'debt', 'mortgage', 'interest',
        'deposit', 'withdrawal', 'account', 'savings', 'checking', 'atm',
        'branch', 'teller', 'overdraft', 'balance', 'statement', 'card',
        'debit', 'credit card', 'apr', 'compound interest', 'simple interest',
        'principal', 'amortization', 'refinancing', 'foreclosure', 'collateral',
        'guarantee', 'co-signer', 'creditworthiness', 'credit score', 'fico',
        'central bank', 'federal reserve', 'monetary policy', 'discount rate',
        'reserve requirement', 'open market operations', 'quantitative easing',
        'commercial bank', 'investment bank', 'retail bank', 'community bank',
        'credit union', 'savings and loan', 'thrift', 'online banking',
        'mobile banking', 'wire transfer', 'ach', 'swift', 'correspondent bank',
        'microfinance', 'microfinance institution', 'microcredit', 'microloan',
        'financial inclusion', 'unbanked', 'underbanked', 'digital banking',
        
        # French banking terms
        'banque', 'bancaire', 'prêt', 'crédit', 'dette', 'hypothèque', 'intérêt',
        'dépôt', 'retrait', 'compte', 'épargne', 'courant', 'distributeur',
        'agence', 'caissier', 'découvert', 'solde', 'relevé', 'carte',
        'débit', 'carte de crédit', 'taux annuel effectif', 'intérêt composé',
        'capital', 'amortissement', 'refinancement', 'saisie', 'garantie',
        'banque centrale', 'politique monétaire', 'taux d\'escompte',
        'banque commerciale', 'banque d\'investissement', 'banque de détail',
        'microfinance', 'institution de microfinance', 'microcrédit', 'microprêt',
        'inclusion financière', 'non bancarisé', 'sous-bancarisé', 'banque numérique',
        
        # Historical banking terms
        'medici bank', 'bank of england', 'first bank of united states',
        'second bank of united states', 'national banking act', 'panic of 1907',
        'federal reserve creation', 'banking act of 1933', 'fdic creation',
        'savings and loan crisis', 'continental illinois', 'long-term capital',
        'banking history', 'central banking history', 'monetary history',
        'bank runs', 'bank failures', 'deposit insurance', 'bank regulation history'
    ],
    
    'economics': [
        # English economics terms
        'economic', 'economics', 'economy', 'gdp', 'gnp', 'inflation', 'deflation',
        'market', 'supply', 'demand', 'recession', 'depression', 'growth', 'unemployment',
        'trade', 'import', 'export', 'currency', 'exchange rate', 'forex',
        'monetary policy', 'fiscal policy', 'macroeconomic', 'microeconomic',
        'elasticity', 'equilibrium', 'consumer', 'producer', 'competition',
        'monopoly', 'oligopoly', 'perfect competition', 'market failure',
        'externality', 'public goods', 'merit goods', 'demerit goods',
        'opportunity cost', 'comparative advantage', 'absolute advantage',
        'productivity', 'efficiency', 'pareto optimal', 'deadweight loss',
        'consumer surplus', 'producer surplus', 'price discrimination',
        'keynesian', 'classical', 'neoclassical', 'austrian school',
        'chicago school', 'monetarism', 'supply-side', 'behavioral economics',
        'development economics', 'economic development', 'emerging markets',
        'economic indicators', 'leading indicators', 'lagging indicators',
        
        # French economics terms
        'économique', 'économie', 'pib', 'pnb', 'inflation', 'déflation',
        'marché', 'offre', 'demande', 'récession', 'croissance', 'chômage',
        'commerce', 'importation', 'exportation', 'devise', 'taux de change',
        'politique monétaire', 'politique fiscale', 'macroéconomique', 'microéconomique',
        'élasticité', 'équilibre', 'consommateur', 'producteur', 'concurrence',
        'monopole', 'oligopole', 'concurrence parfaite', 'défaillance du marché',
        'externalité', 'biens publics', 'coût d\'opportunité', 'avantage comparatif',
        'productivité', 'efficacité', 'surplus du consommateur',
        'économie du développement', 'développement économique', 'marchés émergents',
        'indicateurs économiques', 'indicateurs avancés', 'indicateurs retardés',
        
        # Historical economics terms
        'adam smith', 'wealth of nations', 'invisible hand', 'david ricardo',
        'thomas malthus', 'john stuart mill', 'karl marx', 'das kapital',
        'alfred marshall', 'john maynard keynes', 'general theory',
        'friedrich hayek', 'milton friedman', 'joseph schumpeter',
        'paul samuelson', 'gary becker', 'history of economic thought',
        'economic schools', 'mercantilism', 'physiocracy', 'classical economics',
        'great depression economics', 'new deal', 'stagflation', 'supply-side revolution'
    ],
    
    'fiscal': [
        # English fiscal terms
        'fiscal', 'tax', 'taxation', 'government spending', 'public finance',
        'budget deficit', 'budget surplus', 'national debt', 'debt ceiling', 'treasury',
        'treasury bonds', 'treasury bills', 'treasury notes', 'municipal bonds',
        'federal budget', 'state budget', 'local budget', 'appropriation',
        'revenue', 'expenditure', 'entitlement', 'discretionary spending',
        'mandatory spending', 'social security', 'medicare', 'medicaid',
        'irs', 'internal revenue service', 'tax code', 'tax reform',
        'deduction', 'exemption', 'credit', 'withholding', 'estimated tax',
        'corporate tax', 'income tax', 'property tax', 'sales tax',
        'excise tax', 'capital gains tax', 'estate tax', 'gift tax',
        'payroll tax', 'alternative minimum tax', 'flat tax', 'progressive tax',
        'regressive tax', 'proportional tax', 'tax incidence', 'tax burden',
        'fiscal stimulus', 'austerity', 'deficit spending', 'balanced budget',
        
        # French fiscal terms
        'fiscal', 'impôt', 'taxation', 'dépenses publiques', 'finances publiques',
        'déficit budgétaire', 'excédent budgétaire', 'dette publique', 'trésor public',
        'obligations d\'état', 'bons du trésor', 'obligations municipales',
        'budget fédéral', 'budget de l\'état', 'recettes', 'dépenses',
        'sécurité sociale', 'déduction', 'exemption', 'crédit d\'impôt',
        'impôt sur les sociétés', 'impôt sur le revenu', 'impôt foncier',
        'taxe sur la valeur ajoutée', 'tva', 'impôt progressif', 'impôt proportionnel',
        'stimulus fiscal', 'austérité', 'dépenses déficitaires', 'budget équilibré',
        
        # Historical fiscal terms
        'tax history', 'income tax history', 'revenue act', 'tax reform act',
        'sixteenth amendment', 'internal revenue act', 'war revenue act',
        'new deal taxation', 'tax cuts and jobs act', 'economic recovery tax act',
        'tax reform act of 1986', 'american taxpayer relief act',
        'history of taxation', 'fiscal policy history', 'budget history',
        'deficit spending history', 'debt ceiling history'
    ],
    
    'legal_financial': [
        # English legal financial terms
        'juridical', 'jurisdiction', 'legal', 'law', 'regulation', 'compliance',
        'audit', 'auditor', 'sec', 'securities and exchange commission',
        'cftc', 'commodity futures trading commission', 'finra', 'fdic',
        'occ', 'office of comptroller of currency', 'financial law',
        'securities law', 'banking law', 'insurance law', 'contract law',
        'corporate law', 'commercial law', 'bankruptcy law', 'tax law',
        'antitrust law', 'consumer protection', 'fair lending', 'truth in lending',
        'fair credit reporting act', 'equal credit opportunity act',
        'community reinvestment act', 'bank secrecy act', 'patriot act',
        'money laundering', 'know your customer', 'kyc', 'aml',
        'fiduciary', 'fiduciary duty', 'breach of fiduciary duty',
        'disclosure', 'material disclosure', 'insider trading', 'market manipulation',
        'fraud', 'securities fraud', 'wire fraud', 'mail fraud',
        'ponzi scheme', 'pyramid scheme', 'due diligence', 'regulatory compliance',
        'statute', 'ordinance', 'case law', 'precedent', 'litigation',
        
        # French legal financial terms
        'juridique', 'juridiction', 'légal', 'loi', 'réglementation', 'conformité',
        'audit', 'auditeur', 'droit financier', 'droit des valeurs mobilières',
        'droit bancaire', 'droit des assurances', 'droit des contrats',
        'droit des sociétés', 'droit commercial', 'droit de la faillite',
        'droit fiscal', 'protection du consommateur', 'blanchiment d\'argent',
        'fiduciaire', 'devoir fiduciaire', 'divulgation', 'fraude',
        'manipulation de marché', 'diligence raisonnable', 'conformité réglementaire',
        'statut', 'ordonnance', 'jurisprudence', 'précédent', 'litige',
        
        # Historical legal financial terms
        'securities act of 1933', 'securities exchange act of 1934',
        'investment company act of 1940', 'investment advisers act of 1940',
        'glass-steagall act', 'mcfadden act', 'bank holding company act',
        'riegle-neal act', 'gramm-leach-bliley act', 'sarbanes-oxley act',
        'dodd-frank act', 'volcker rule', 'basel i', 'basel ii', 'basel iii',
        'mifid', 'mifid ii', 'psd2', 'gdpr financial', 'financial regulation history',
        'securities law history', 'banking law history', 'regulatory evolution'
    ],
    
    'analysis': [
        # English analysis terms
        'analysis', 'analyze', 'analytical', 'statistical', 'statistics', 'stats',
        'data', 'dataset', 'database', 'big data', 'data mining', 'data science',
        'trend', 'trending', 'pattern', 'correlation', 'causation', 'regression',
        'linear regression', 'multiple regression', 'logistic regression',
        'forecast', 'forecasting', 'predict', 'prediction', 'predictive',
        'model', 'modeling', 'simulation', 'monte carlo', 'scenario analysis',
        'sensitivity analysis', 'stress testing', 'backtesting',
        'visualization', 'chart', 'graph', 'plot', 'histogram', 'scatter plot',
        'time series', 'dashboard', 'reporting', 'report', 'insight',
        'metric', 'kpi', 'key performance indicator', 'benchmark', 'benchmarking',
        'performance', 'analytics', 'business analytics', 'financial analytics',
        'sample', 'population', 'hypothesis', 'hypothesis testing',
        'significance', 'p-value', 'confidence interval', 'chi-square',
        't-test', 'anova', 'variance analysis', 'factor analysis',
        'cluster analysis', 'discriminant analysis', 'principal component analysis',
        
        # French analysis terms
        'analyse', 'analyser', 'analytique', 'statistique', 'statistiques',
        'données', 'base de données', 'exploration de données', 'science des données',
        'tendance', 'modèle', 'corrélation', 'régression', 'prévision',
        'prédiction', 'modélisation', 'simulation', 'visualisation',
        'graphique', 'tableau de bord', 'rapport', 'aperçu', 'métrique',
        'indicateur de performance', 'référence', 'performance', 'analytique',
        'échantillon', 'population', 'hypothèse', 'test d\'hypothèse',
        'signification', 'intervalle de confiance', 'analyse de variance',
        'analyse factorielle', 'analyse de cluster',
        
        # Historical analysis terms
        'history of statistics', 'statistical methods history', 'econometrics history',
        'financial analysis history', 'quantitative analysis evolution',
        'computational finance history', 'risk management evolution',
        'portfolio theory history', 'modern portfolio theory', 'capm history',
        'efficient market hypothesis', 'behavioral finance history',
        'technical analysis history', 'fundamental analysis history'
    ],
    
    'mathematics': [
        # English mathematics terms
        'math', 'mathematics', 'mathematical', 'maths', 'calculate', 'calculation',
        'compute', 'computation', 'computational', 'algorithm', 'algorithmic',
        'formula', 'formulae', 'equation', 'expression', 'function',
        'variable', 'constant', 'parameter', 'coefficient', 'exponent',
        'logarithm', 'exponential', 'polynomial', 'quadratic', 'cubic',
        'probability', 'distribution', 'normal distribution', 'binomial',
        'poisson', 'uniform', 'chi-square', 'variance', 'standard deviation',
        'mean', 'median', 'mode', 'sum', 'average', 'weighted average',
        'percentage', 'percent', 'ratio', 'proportion', 'rate',
        'derivative', 'differential', 'integral', 'calculus', 'limit',
        'matrix', 'matrices', 'vector', 'linear algebra', 'eigenvalue',
        'eigenvector', 'determinant', 'inverse', 'transpose',
        'geometry', 'trigonometry', 'algebra', 'arithmetic', 'number theory',
        'discrete mathematics', 'combinatorics', 'permutation', 'combination',
        'optimization', 'linear programming', 'game theory', 'set theory',
        'probability theory', 'bayesian', 'frequentist', 'conditional probability',
        'bayes theorem', 'law of total probability', 'independence',
        
        # French mathematics terms
        'mathématiques', 'mathématique', 'maths', 'calculer', 'calcul',
        'computation', 'algorithme', 'formule', 'équation', 'expression',
        'fonction', 'variable', 'constante', 'paramètre', 'coefficient',
        'logarithme', 'exponentiel', 'polynôme', 'quadratique',
        'probabilité', 'distribution', 'distribution normale', 'variance',
        'écart-type', 'moyenne', 'médiane', 'mode', 'somme', 'pourcentage',
        'rapport', 'proportion', 'taux', 'dérivée', 'différentiel',
        'intégrale', 'calcul', 'limite', 'matrice', 'vecteur',
        'algèbre linéaire', 'valeur propre', 'vecteur propre', 'déterminant',
        'géométrie', 'trigonométrie', 'algèbre', 'arithmétique',
        'optimisation', 'programmation linéaire', 'théorie des jeux',
        'théorie des probabilités', 'bayésien', 'fréquentiste', 'probabilité conditionnelle',
        'théorème de bayes', 'loi de probabilité totale', 'indépendance',
        
        # Historical mathematics terms
        'history of mathematics', 'mathematical history', 'ancient mathematics',
        'greek mathematics', 'babylonian mathematics', 'egyptian mathematics',
        'indian mathematics', 'chinese mathematics', 'islamic mathematics',
        'european mathematics', 'renaissance mathematics', 'modern mathematics',
        'euler', 'gauss', 'newton', 'leibniz', 'fermat', 'pascal',
        'fibonacci', 'pythagoras', 'euclid', 'archimedes', 'mathematical evolution',
        'calculus history', 'algebra history', 'geometry history', 'number theory history'
    ],

    'technology_data': [
        # English technology terms (data-related only)
        'python', 'r', 'sql', 'database', 'query', 'pandas', 'numpy', 'scipy',
        'scikit-learn', 'sklearn', 'tensorflow', 'pytorch', 'keras',
        'jupyter', 'notebook', 'jupyter notebook', 'colab', 'rstudio',
        'excel', 'spreadsheet', 'csv', 'json', 'xml', 'parquet',
        'api', 'rest api', 'web scraping', 'data extraction',
        'cloud computing', 'aws', 'azure', 'google cloud', 'gcp',
        'big data', 'hadoop', 'spark', 'data warehouse', 'data lake',
        'etl tool', 'data integration', 'data migration',
        'version control', 'git', 'github', 'gitlab',
        'docker', 'container', 'deployment', 'production',
        
        # French technology terms (data-related only)
        'python', 'r', 'sql', 'base de données', 'requête', 'pandas', 'numpy', 'scipy',
        'scikit-learn', 'sklearn', 'tensorflow', 'pytorch', 'keras',
        'jupyter', 'carnet', 'jupyter notebook', 'colab', 'rstudio',
        'excel', 'tableur', 'csv', 'json', 'xml', 'parquet',
        'api', 'api rest', 'web scraping', 'extraction de données',
        'cloud computing', 'aws', 'azure', 'google cloud', 'gcp',
        'big data', 'hadoop', 'spark', 'entrepôt de données', 'lac de données',
        'outil etl', 'intégration de données', 'migration de données',
        'contrôle de version', 'git', 'github', 'gitlab',
        'docker', 'conteneur', 'déploiement', 'production'
    ],

    'statistics': [
        # English statistics terms
        'statistics', 'statistical', 'stats', 'descriptive statistics', 'inferential statistics',
        'mean', 'average', 'median', 'mode', 'range', 'midrange',
        'variance', 'standard deviation', 'std dev', 'coefficient of variation',
        'skewness', 'kurtosis', 'percentile', 'quartile', 'quintile', 'decile',
        'interquartile range', 'iqr', 'outlier', 'z-score', 'standardization',
        'normalization', 'normal distribution', 'gaussian', 'bell curve',
        'binomial distribution', 'poisson distribution', 'exponential distribution',
        'uniform distribution', 'chi-square distribution', 't-distribution',
        'f-distribution', 'probability', 'likelihood', 'expected value',
        'hypothesis testing', 'null hypothesis', 'alternative hypothesis',
        'p-value', 'significance level', 'alpha', 'confidence interval',
        'confidence level', 't-test', 'z-test', 'chi-square test',
        'anova', 'analysis of variance', 'f-test', 'mann-whitney',
        'wilcoxon', 'kruskal-wallis', 'friedman test', 'kolmogorov-smirnov',
        'shapiro-wilk', 'levene test', 'bartlett test', 'normality test',
        'correlation', 'covariance', 'pearson correlation', 'spearman correlation',
        'kendall tau', 'correlation coefficient', 'correlation matrix',
        'covariance matrix', 'multicollinearity', 'vif', 'variance inflation factor',
        'sample', 'population', 'sampling', 'random sampling', 'stratified sampling',
        'systematic sampling', 'cluster sampling', 'sample size', 'power analysis',
        'central limit theorem', 'law of large numbers', 'standard error',
        'degrees of freedom', 'margin of error', 'bias', 'unbiased estimator',
        
        # French statistics terms
        'statistiques', 'statistique', 'stats', 'statistiques descriptives', 'statistiques inférentielles',
        'moyenne', 'médiane', 'mode', 'étendue', 'intervalle',
        'variance', 'écart-type', 'écart type', 'coefficient de variation',
        'asymétrie', 'aplatissement', 'kurtosis', 'percentile', 'quartile', 'quintile', 'décile',
        'écart interquartile', 'valeur aberrante', 'score z', 'standardisation',
        'normalisation', 'distribution normale', 'gaussienne', 'courbe en cloche',
        'distribution binomiale', 'distribution de poisson', 'distribution exponentielle',
        'distribution uniforme', 'distribution chi-deux', 'distribution t',
        'distribution f', 'probabilité', 'vraisemblance', 'espérance',
        'test d\'hypothèse', 'hypothèse nulle', 'hypothèse alternative',
        'valeur p', 'niveau de signification', 'intervalle de confiance',
        'niveau de confiance', 'test t', 'test z', 'test chi-deux',
        'anova', 'analyse de variance', 'test f', 'mann-whitney',
        'wilcoxon', 'kruskal-wallis', 'test de friedman', 'kolmogorov-smirnov',
        'shapiro-wilk', 'test de levene', 'test de bartlett', 'test de normalité',
        'corrélation', 'covariance', 'corrélation de pearson', 'corrélation de spearman',
        'tau de kendall', 'coefficient de corrélation', 'matrice de corrélation',
        'matrice de covariance', 'multicolinéarité', 'facteur d\'inflation de variance',
        'échantillon', 'population', 'échantillonnage', 'échantillonnage aléatoire',
        'échantillonnage stratifié', 'échantillonnage systématique', 'taille échantillon',
        'théorème central limite', 'loi des grands nombres', 'erreur standard',
        'degrés de liberté', 'marge d\'erreur', 'biais', 'estimateur sans biais'
    ],
    
    'regression': [
        # English regression terms
        'regression', 'regress', 'linear regression', 'simple linear regression',
        'multiple regression', 'multiple linear regression', 'multivariate regression',
        'polynomial regression', 'quadratic regression', 'cubic regression',
        'logistic regression', 'logit', 'binary classification',
        'ridge regression', 'lasso regression', 'elastic net',
        'regularization', 'l1 regularization', 'l2 regularization',
        'ordinary least squares', 'ols', 'least squares', 'sum of squares',
        'residual', 'residuals', 'error term', 'fitted values', 'predicted values',
        'coefficient', 'intercept', 'slope', 'beta coefficient',
        'r-squared', 'r2', 'coefficient of determination', 'adjusted r-squared',
        'goodness of fit', 'residual plot', 'qq plot', 'heteroscedasticity',
        'homoscedasticity', 'autocorrelation', 'durbin-watson',
        'endogeneity', 'instrumental variables', 'two-stage least squares',
        'generalized linear model', 'glm', 'link function', 'probit regression',
        'poisson regression', 'negative binomial regression', 'cox regression',
        'survival analysis', 'hazard ratio', 'kaplan-meier',
        'time series regression', 'autoregressive', 'ar', 'moving average', 'ma',
        'stepwise regression', 'forward selection', 'backward elimination',
        'cross-validation', 'train test split', 'overfitting', 'underfitting',
        
        # French regression terms
        'régression', 'régresser', 'régression linéaire', 'régression linéaire simple',
        'régression multiple', 'régression linéaire multiple', 'régression multivariée',
        'régression polynomiale', 'régression quadratique', 'régression cubique',
        'régression logistique', 'logit', 'classification binaire',
        'régression ridge', 'régression lasso', 'elastic net',
        'régularisation', 'régularisation l1', 'régularisation l2',
        'moindres carrés ordinaires', 'mco', 'moindres carrés', 'somme des carrés',
        'résidu', 'résidus', 'terme d\'erreur', 'valeurs ajustées', 'valeurs prédites',
        'coefficient', 'ordonnée à l\'origine', 'pente', 'coefficient bêta',
        'r carré', 'r2', 'coefficient de détermination', 'r carré ajusté',
        'qualité d\'ajustement', 'graphique résiduel', 'graphique qq', 'hétéroscédasticité',
        'homoscédasticité', 'autocorrélation', 'durbin-watson',
        'endogénéité', 'variables instrumentales', 'doubles moindres carrés',
        'modèle linéaire généralisé', 'glm', 'fonction de lien', 'régression probit',
        'régression de poisson', 'régression binomiale négative', 'régression de cox',
        'analyse de survie', 'rapport de risque', 'kaplan-meier',
        'régression temporelle', 'autorégressif', 'moyenne mobile',
        'régression pas à pas', 'sélection avant', 'élimination arrière',
        'validation croisée', 'division train test', 'surapprentissage', 'sous-apprentissage'
    ],
    
    'machine_learning': [
        # English ML terms
        'machine learning', 'ml', 'artificial intelligence', 'ai', 'deep learning',
        'neural network', 'supervised learning', 'unsupervised learning',
        'reinforcement learning', 'semi-supervised', 'transfer learning',
        'random forest', 'decision tree', 'gradient boosting', 'xgboost',
        'adaboost', 'lightgbm', 'catboost', 'ensemble method', 'bagging', 'boosting',
        'k-nearest neighbors', 'knn', 'k-means', 'kmeans clustering',
        'support vector machine', 'svm', 'kernel', 'kernel trick',
        'naive bayes', 'gaussian naive bayes', 'multinomial naive bayes',
        'classification', 'classifier', 'binary classification', 'multiclass',
        'confusion matrix', 'accuracy', 'precision', 'recall', 'f1 score',
        'sensitivity', 'specificity', 'roc curve', 'auc', 'area under curve',
        'true positive', 'false positive', 'true negative', 'false negative',
        'training set', 'test set', 'validation set', 'holdout', 'k-fold',
        'cross validation', 'stratified k-fold', 'leave-one-out',
        'hyperparameter', 'hyperparameter tuning', 'grid search', 'random search',
        'feature engineering', 'feature selection', 'feature extraction',
        'feature importance', 'feature scaling', 'one-hot encoding',
        'label encoding', 'embedding', 'dimensionality reduction',
        'bias-variance tradeoff', 'model selection', 'model evaluation',
        'overfitting', 'underfitting', 'regularization', 'dropout',
        'batch normalization', 'activation function', 'relu', 'sigmoid', 'tanh',
        'softmax', 'loss function', 'cost function', 'optimizer',
        'gradient descent', 'stochastic gradient descent', 'adam', 'momentum',
        'backpropagation', 'forward propagation', 'epoch', 'batch size',
        'learning rate', 'convergence', 'early stopping',
        
        # French ML terms
        'apprentissage automatique', 'apprentissage machine', 'intelligence artificielle',
        'ia', 'apprentissage profond', 'réseau neuronal', 'réseau de neurones',
        'apprentissage supervisé', 'apprentissage non supervisé',
        'apprentissage par renforcement', 'apprentissage semi-supervisé', 'transfert d\'apprentissage',
        'forêt aléatoire', 'arbre de décision', 'gradient boosting', 'xgboost',
        'méthode d\'ensemble', 'bagging', 'boosting',
        'k plus proches voisins', 'knn', 'k-means', 'clustering k-means',
        'machine à vecteurs de support', 'svm', 'noyau', 'astuce du noyau',
        'naive bayes', 'bayes naïf', 'classification naïve bayésienne',
        'classification', 'classificateur', 'classification binaire', 'multiclasse',
        'matrice de confusion', 'exactitude', 'précision', 'rappel', 'score f1',
        'sensibilité', 'spécificité', 'courbe roc', 'auc', 'aire sous la courbe',
        'vrai positif', 'faux positif', 'vrai négatif', 'faux négatif',
        'ensemble d\'entraînement', 'ensemble de test', 'ensemble de validation',
        'validation croisée', 'validation croisée k-fold', 'validation croisée stratifiée',
        'hyperparamètre', 'réglage hyperparamètres', 'recherche en grille', 'recherche aléatoire',
        'ingénierie des caractéristiques', 'sélection des caractéristiques', 'extraction caractéristiques',
        'importance des caractéristiques', 'mise à l\'échelle', 'encodage one-hot',
        'encodage d\'étiquette', 'plongement', 'réduction de dimensionnalité',
        'compromis biais-variance', 'sélection de modèle', 'évaluation de modèle',
        'surapprentissage', 'sous-apprentissage', 'régularisation', 'dropout',
        'normalisation par lot', 'fonction d\'activation', 'relu', 'sigmoïde', 'tanh',
        'softmax', 'fonction de perte', 'fonction de coût', 'optimiseur',
        'descente de gradient', 'descente de gradient stochastique', 'adam', 'momentum',
        'rétropropagation', 'propagation avant', 'époque', 'taille de lot',
        'taux d\'apprentissage', 'convergence', 'arrêt précoce'
    ],
    
    'dimensionality_reduction': [
        # English dimensionality reduction terms
        'dimensionality reduction', 'dimension reduction', 'feature reduction',
        'principal component analysis', 'pca', 'principal components',
        'eigenvalue', 'eigenvector', 'eigendecomposition', 'spectral decomposition',
        'singular value decomposition', 'svd', 'latent variables',
        'scree plot', 'explained variance', 'cumulative variance',
        'loading', 'factor loading', 'component loading', 'rotation',
        'varimax', 'oblimin', 'factor analysis', 'exploratory factor analysis',
        'confirmatory factor analysis', 'efa', 'cfa',
        'multiple correspondence analysis', 'mca', 'correspondence analysis',
        't-sne', 't-distributed stochastic neighbor embedding', 'tsne',
        'umap', 'uniform manifold approximation', 'manifold learning',
        'isomap', 'locally linear embedding', 'lle', 'autoencoder',
        'latent dirichlet allocation', 'lda', 'topic modeling',
        'independent component analysis', 'ica', 'blind source separation',
        'non-negative matrix factorization', 'nmf', 'matrix factorization',
        'truncated svd', 'incremental pca', 'kernel pca', 'sparse pca',
        
        # French dimensionality reduction terms
        'réduction de dimensionnalité', 'réduction de dimension', 'réduction caractéristiques',
        'analyse en composantes principales', 'acp', 'composantes principales',
        'valeur propre', 'vecteur propre', 'décomposition propre', 'décomposition spectrale',
        'décomposition en valeurs singulières', 'svd', 'variables latentes',
        'graphique d\'éboulis', 'variance expliquée', 'variance cumulée',
        'chargement', 'chargement factoriel', 'chargement composante', 'rotation',
        'varimax', 'oblimin', 'analyse factorielle', 'analyse factorielle exploratoire',
        'analyse factorielle confirmatoire', 'efa', 'cfa',
        'analyse des correspondances multiples', 'acm', 'analyse des correspondances',
        't-sne', 'plongement stochastique voisin distribué t', 'tsne',
        'umap', 'approximation uniforme de variété', 'apprentissage de variété',
        'isomap', 'plongement linéaire local', 'lle', 'autoencodeur',
        'allocation de dirichlet latente', 'lda', 'modélisation de sujets',
        'analyse en composantes indépendantes', 'ica', 'séparation de sources aveugles',
        'factorisation matricielle non négative', 'nmf', 'factorisation matricielle',
        'svd tronqué', 'acp incrémentale', 'acp noyau', 'acp sparse'
    ],
    
    'clustering': [
        # English clustering terms
        'clustering', 'cluster analysis', 'unsupervised clustering',
        'k-means', 'kmeans', 'k-means clustering', 'centroid',
        'hierarchical clustering', 'hierarchical agglomerative clustering', 'hac',
        'dendrogram', 'linkage', 'single linkage', 'complete linkage',
        'average linkage', 'ward linkage', 'ward method',
        'dbscan', 'density-based clustering', 'eps', 'min samples',
        'optics', 'mean shift', 'affinity propagation', 'spectral clustering',
        'gaussian mixture model', 'gmm', 'expectation maximization', 'em algorithm',
        'fuzzy c-means', 'fuzzy clustering', 'soft clustering', 'hard clustering',
        'elbow method', 'silhouette score', 'silhouette analysis',
        'davies-bouldin index', 'calinski-harabasz', 'dunn index',
        'cluster validation', 'cluster quality', 'optimal clusters',
        'inertia', 'within-cluster sum of squares', 'wcss',
        'between-cluster variance', 'separation', 'compactness',
        
        # French clustering terms
        'clustering', 'regroupement', 'analyse de clusters', 'classification non supervisée',
        'k-means', 'kmeans', 'classification k-means', 'centroïde',
        'classification hiérarchique', 'classification hiérarchique agglomérative', 'hac',
        'dendrogramme', 'liaison', 'liaison simple', 'liaison complète',
        'liaison moyenne', 'liaison ward', 'méthode ward',
        'dbscan', 'classification basée sur la densité', 'eps', 'échantillons min',
        'optics', 'mean shift', 'propagation d\'affinité', 'classification spectrale',
        'modèle de mélange gaussien', 'gmm', 'maximisation de l\'espérance', 'algorithme em',
        'c-means flou', 'classification floue', 'classification douce', 'classification dure',
        'méthode du coude', 'score silhouette', 'analyse silhouette',
        'indice davies-bouldin', 'calinski-harabasz', 'indice de dunn',
        'validation clusters', 'qualité clusters', 'clusters optimaux',
        'inertie', 'somme des carrés intra-cluster', 'wcss',
        'variance inter-cluster', 'séparation', 'compacité'
    ],
    
    'time_series': [
        # English time series terms
        'time series', 'time series analysis', 'temporal data', 'longitudinal data',
        'trend', 'seasonality', 'seasonal', 'cyclical', 'irregular',
        'decomposition', 'seasonal decomposition', 'additive model', 'multiplicative model',
        'moving average', 'simple moving average', 'sma', 'exponential moving average', 'ema',
        'weighted moving average', 'wma', 'exponential smoothing',
        'single exponential smoothing', 'double exponential smoothing', 'holt method',
        'triple exponential smoothing', 'holt-winters', 'seasonal smoothing',
        'arima', 'autoregressive integrated moving average',
        'arma', 'autoregressive moving average', 'ar', 'autoregressive model',
        'ma', 'moving average model', 'pacf', 'partial autocorrelation',
        'acf', 'autocorrelation function', 'autocorrelation', 'lag',
        'differencing', 'first difference', 'seasonal differencing',
        'stationarity', 'stationary', 'non-stationary', 'unit root',
        'augmented dickey-fuller', 'adf test', 'kpss test', 'phillips-perron',
        'sarima', 'seasonal arima', 'sarimax', 'exogenous variables',
        'var', 'vector autoregression', 'vecm', 'error correction model',
        'granger causality', 'impulse response', 'forecast', 'forecasting',
        'out-of-sample', 'rolling forecast', 'walk-forward validation',
        'mape', 'mean absolute percentage error', 'mae', 'mean absolute error',
        'rmse', 'root mean squared error', 'mse', 'mean squared error',
        
        # French time series terms
        'série temporelle', 'analyse de séries temporelles', 'données temporelles', 'données longitudinales',
        'tendance', 'saisonnalité', 'saisonnier', 'cyclique', 'irrégulier',
        'décomposition', 'décomposition saisonnière', 'modèle additif', 'modèle multiplicatif',
        'moyenne mobile', 'moyenne mobile simple', 'mms', 'moyenne mobile exponentielle', 'mme',
        'moyenne mobile pondérée', 'mmp', 'lissage exponentiel',
        'lissage exponentiel simple', 'lissage exponentiel double', 'méthode holt',
        'lissage exponentiel triple', 'holt-winters', 'lissage saisonnier',
        'arima', 'moyenne mobile intégrée autorégressive',
        'arma', 'moyenne mobile autorégressive', 'ar', 'modèle autorégressif',
        'ma', 'modèle moyenne mobile', 'pacf', 'autocorrélation partielle',
        'acf', 'fonction d\'autocorrélation', 'autocorrélation', 'décalage',
        'différenciation', 'première différence', 'différenciation saisonnière',
        'stationnarité', 'stationnaire', 'non-stationnaire', 'racine unitaire',
        'dickey-fuller augmenté', 'test adf', 'test kpss', 'phillips-perron',
        'sarima', 'arima saisonnier', 'sarimax', 'variables exogènes',
        'var', 'autorégression vectorielle', 'vecm', 'modèle correction erreur',
        'causalité de granger', 'réponse impulsionnelle', 'prévision', 'prévisions',
        'hors échantillon', 'prévision glissante', 'validation forward',
        'mape', 'erreur absolue moyenne en pourcentage', 'mae', 'erreur absolue moyenne',
        'rmse', 'racine erreur quadratique moyenne', 'mse', 'erreur quadratique moyenne'
    ],

     'data_visualization': [
        # English visualization terms
        'visualization', 'visualize', 'visualisation', 'visualise', 'chart', 'graph', 'plot',
        'line chart', 'line graph', 'line plot', 'bar chart', 'bar graph', 'histogram',
        'pie chart', 'donut chart', 'scatter plot', 'scatter chart', 'bubble chart',
        'box plot', 'boxplot', 'box and whisker', 'violin plot', 'swarm plot',
        'heatmap', 'heat map', 'correlation heatmap', 'contour plot',
        'area chart', 'stacked area', 'stream graph', 'sankey diagram',
        'treemap', 'sunburst', 'radial chart', 'radar chart', 'spider chart',
        'gantt chart', 'waterfall chart', 'funnel chart', 'gauge chart',
        'candlestick', 'ohlc', 'time series plot', 'sparkline',
        'interactive plot', 'interactive visualization', 'dashboard',
        'plotly', 'matplotlib', 'seaborn', 'bokeh', 'altair', 'd3',
        'tableau', 'power bi', 'qlik', 'looker', 'grafana',
        'color scale', 'color palette', 'gradient', 'legend', 'axis',
        'x-axis', 'y-axis', 'z-axis', 'title', 'label', 'annotation',
        'tooltip', 'hover', 'zoom', 'pan', 'filter', 'drill-down',
        
        # French visualization terms
        'visualisation', 'visualiser', 'graphique', 'diagramme', 'tracé',
        'graphique linéaire', 'graphique à lignes', 'graphique à barres', 'histogramme',
        'diagramme circulaire', 'diagramme en anneau', 'nuage de points', 'graphique à bulles',
        'boîte à moustaches', 'diagramme en boîte', 'diagramme violon', 'diagramme essaim',
        'carte thermique', 'carte de chaleur', 'carte thermique corrélation', 'tracé de contour',
        'graphique en aires', 'aires empilées', 'diagramme de flux', 'diagramme sankey',
        'treemap', 'diagramme en rayons de soleil', 'graphique radial', 'graphique radar', 'graphique araignée',
        'diagramme de gantt', 'graphique en cascade', 'graphique entonnoir', 'jauge',
        'chandelier', 'ohlc', 'tracé série temporelle', 'sparkline',
        'tracé interactif', 'visualisation interactive', 'tableau de bord',
        'plotly', 'matplotlib', 'seaborn', 'bokeh', 'altair', 'd3',
        'tableau', 'power bi', 'qlik', 'looker', 'grafana',
        'échelle de couleurs', 'palette de couleurs', 'dégradé', 'légende', 'axe',
        'axe x', 'axe y', 'axe z', 'titre', 'étiquette', 'annotation',
        'infobulle', 'survol', 'zoom', 'panoramique', 'filtre', 'exploration'
    ],
    
    'data_processing': [
        # English data processing terms
        'data processing', 'data manipulation', 'data wrangling', 'data munging',
        'etl', 'extract transform load', 'data pipeline', 'data workflow',
        'data cleaning', 'data cleansing', 'data preprocessing', 'data preparation',
        'missing data', 'missing values', 'null values', 'nan', 'imputation',
        'mean imputation', 'median imputation', 'mode imputation', 'forward fill',
        'backward fill', 'interpolation', 'linear interpolation', 'spline interpolation',
        'outlier detection', 'outlier removal', 'anomaly detection', 'anomalies',
        'data validation', 'data quality', 'data integrity', 'data consistency',
        'duplicate records', 'duplicates', 'deduplication', 'data merge', 'data join',
        'inner join', 'outer join', 'left join', 'right join', 'cross join',
        'concatenation', 'append', 'union', 'intersection', 'difference',
        'groupby', 'group by', 'aggregation', 'aggregate', 'pivot', 'pivot table',
        'unpivot', 'melt', 'reshape', 'transpose', 'wide format', 'long format',
        'sorting', 'filtering', 'subsetting', 'slicing', 'indexing',
        'binning', 'discretization', 'categorical encoding', 'dummy variables',
        'data type conversion', 'casting', 'parsing', 'string manipulation',
        'regex', 'regular expression', 'pattern matching', 'text processing',
        
        # French data processing terms
        'traitement de données', 'manipulation de données', 'nettoyage de données',
        'etl', 'extraction transformation chargement', 'pipeline de données', 'flux de travail données',
        'nettoyage données', 'prétraitement données', 'préparation données',
        'données manquantes', 'valeurs manquantes', 'valeurs nulles', 'nan', 'imputation',
        'imputation moyenne', 'imputation médiane', 'imputation mode', 'remplissage avant',
        'remplissage arrière', 'interpolation', 'interpolation linéaire', 'interpolation spline',
        'détection valeurs aberrantes', 'suppression valeurs aberrantes', 'détection anomalies', 'anomalies',
        'validation données', 'qualité données', 'intégrité données', 'cohérence données',
        'enregistrements dupliqués', 'doublons', 'déduplication', 'fusion données', 'jointure données',
        'jointure interne', 'jointure externe', 'jointure gauche', 'jointure droite', 'jointure croisée',
        'concaténation', 'ajouter', 'union', 'intersection', 'différence',
        'grouper par', 'agrégation', 'agréger', 'pivot', 'tableau croisé',
        'dépivot', 'fondre', 'remodeler', 'transposer', 'format large', 'format long',
        'tri', 'filtrage', 'sous-ensemble', 'découpage', 'indexation',
        'binning', 'discrétisation', 'encodage catégoriel', 'variables indicatrices',
        'conversion type données', 'casting', 'analyse', 'manipulation chaînes',
        'regex', 'expression régulière', 'correspondance motifs', 'traitement texte'
    ],
}

# Classification prompt for OpenAI
CLASSIFICATION_PROMPT = """You are a question classifier for DataStats, a specialized financial and analytical AI assistant developed by BEAC (Banque des États de l'Afrique Centrale).

Determine if the following question is related to any of these ALLOWED domains:

ALLOWED DOMAINS:
✅ DataStats application features, usage, and capabilities
✅ Financial analysis, banking, finance, economics, investments
✅ Microfinance, financial institutions, bank data processing
✅ Statistical analysis, hypothesis testing, distributions
✅ Regression models (linear, logistic, polynomial, ridge, lasso)
✅ Machine learning (Random Forest, KNN, classification, clustering)
✅ Dimensionality reduction (PCA, MCA, eigenvalues, scree plots)
✅ Time series analysis (ARIMA, moving averages, forecasting)
✅ Data visualization (charts, plots, heatmaps, dashboards)
✅ Data processing, cleaning, transformation, ETL
✅ Mathematical calculations, algorithms, optimization
✅ Matrix operations, correlation, covariance analysis
✅ Data-related technology (Python, R, SQL, Excel, databases)
✅ Basic greetings and polite conversation

RESTRICTED DOMAINS:
❌ Sports, entertainment, movies, music, celebrities
❌ Cooking, recipes, food, restaurants (unless economic analysis)
❌ Travel, tourism (unless economic/financial context)
❌ Non-data technology (gaming, social media, hardware)
❌ Health, medicine, fitness (unless health economics/statistics)
❌ Politics (unless economic policy or fiscal matters)
❌ General trivia, history (unless economic/financial history)
❌ Personal advice (unless financial planning)

IMPORTANT: Questions about DataStats, BEAC, data analysis, statistics, finance, economics, and mathematical modeling are ALWAYS allowed. Be strict with other topics.

Respond with EXACTLY one word: either "ALLOWED" or "RESTRICTED"

Question to classify:"""

# Restriction response message (bilingual)
RESTRICTION_MESSAGE = """I'm DataStats AI, a specialized AI assistant for financial and analytical domains developed for BEAC. 

Je suis DataStats, un assistant IA spécialisé dans les domaines financiers et analytiques développé pour la BEAC.

I can help you with / Je peux vous aider avec:

🏦 **Banking & Finance / Banque & Finance**: Investments, portfolios, financial planning, microfinance / Investissements, portefeuilles, planification financière, microfinance

📊 **Statistical Analysis / Analyse Statistique**: Descriptive stats, hypothesis testing, distributions / Statistiques descriptives, tests d'hypothèses, distributions

📈 **Regression & ML / Régression & ML**: Linear/logistic regression, Random Forest, KNN / Régression linéaire/logistique, forêts aléatoires, KNN

🔢 **Data Analysis / Analyse de Données**: PCA, clustering, time series, visualization / ACP, clustering, séries temporelles, visualisation

💻 **DataStats App**: Features, usage, data upload, report generation / Fonctionnalités, utilisation, téléchargement données, génération rapports

💰 **Economics & Fiscal / Économie & Fiscal**: Economic indicators, fiscal policy, taxation / Indicateurs économiques, politique fiscale, taxation

Please ask me something related to these areas! / Veuillez me poser une question liée à ces domaines!
"""

# Enhanced system context
ENHANCED_SYSTEM_CONTEXT = """You are a specialized AI assistant focused on financial, economic, and analytical domains. 

Your expertise includes:
- Financial analysis, banking, and investment guidance
- Economic trends, fiscal policy, and market analysis  
- Mathematical calculations and statistical analysis
- Data analysis, visualization, and pattern recognition
- Financial regulations and compliance matters

STRICT RULES:
- ONLY answer questions within your specialized domains
- If asked about unrelated topics, politely redirect to your areas of expertise
- Always provide accurate, helpful information within your domain
- Explain complex concepts in simple, understandable terms
- Maintain a professional but friendly tone"""