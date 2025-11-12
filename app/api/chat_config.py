# app/api/chat_config.py
"""
Configuration file for chatbot domain restrictions
"""

# Define extended allowed domain keywords for comprehensive filtering
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
        
        # French finance terms
        'finance', 'financier', 'argent', 'investissement', 'portefeuille', 'actif',
        'passif', 'capitaux propres', 'profit', 'perte', 'revenus', 'dépenses',
        'budget', 'coût', 'prix', 'valeur', 'évaluation', 'flux de trésorerie',
        'retour sur investissement', 'dividende', 'action', 'obligation', 'titre',
        'capital', 'financement', 'capital-risque', 'fonds propres',
        'bourse', 'marché', 'courtier', 'négociant', 'liquidité', 'volatilité',
        'risque', 'diversification', 'rendement', 'échéance', 'arbitrage',
        
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
        
        # French banking terms
        'banque', 'bancaire', 'prêt', 'crédit', 'dette', 'hypothèque', 'intérêt',
        'dépôt', 'retrait', 'compte', 'épargne', 'courant', 'distributeur',
        'agence', 'caissier', 'découvert', 'solde', 'relevé', 'carte',
        'débit', 'carte de crédit', 'taux annuel effectif', 'intérêt composé',
        'capital', 'amortissement', 'refinancement', 'saisie', 'garantie',
        'banque centrale', 'politique monétaire', 'taux d\'escompte',
        'banque commerciale', 'banque d\'investissement', 'banque de détail',
        
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
        
        # French economics terms
        'économique', 'économie', 'pib', 'pnb', 'inflation', 'déflation',
        'marché', 'offre', 'demande', 'récession', 'croissance', 'chômage',
        'commerce', 'importation', 'exportation', 'devise', 'taux de change',
        'politique monétaire', 'politique fiscale', 'macroéconomique', 'microéconomique',
        'élasticité', 'équilibre', 'consommateur', 'producteur', 'concurrence',
        'monopole', 'oligopole', 'concurrence parfaite', 'défaillance du marché',
        'externalité', 'biens publics', 'coût d\'opportunité', 'avantage comparatif',
        'productivité', 'efficacité', 'surplus du consommateur',
        
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
        
        # French fiscal terms
        'fiscal', 'impôt', 'taxation', 'dépenses publiques', 'finances publiques',
        'déficit budgétaire', 'excédent budgétaire', 'dette publique', 'trésor public',
        'obligations d\'état', 'bons du trésor', 'obligations municipales',
        'budget fédéral', 'budget de l\'état', 'recettes', 'dépenses',
        'sécurité sociale', 'déduction', 'exemption', 'crédit d\'impôt',
        'impôt sur les sociétés', 'impôt sur le revenu', 'impôt foncier',
        'taxe sur la valeur ajoutée', 'tva', 'impôt progressif', 'impôt proportionnel',
        
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
        
        # Historical mathematics terms
        'history of mathematics', 'mathematical history', 'ancient mathematics',
        'greek mathematics', 'babylonian mathematics', 'egyptian mathematics',
        'indian mathematics', 'chinese mathematics', 'islamic mathematics',
        'european mathematics', 'renaissance mathematics', 'modern mathematics',
        'euler', 'gauss', 'newton', 'leibniz', 'fermat', 'pascal',
        'fibonacci', 'pythagoras', 'euclid', 'archimedes', 'mathematical evolution',
        'calculus history', 'algebra history', 'geometry history', 'number theory history'
    ]
}

# Classification prompt for OpenAI
CLASSIFICATION_PROMPT = """You are a question classifier for a specialized financial and analytical AI assistant. 

Determine if the following question is related to any of these ALLOWED domains:

ALLOWED DOMAINS:
✅ Financial analysis, banking, finance, economics, investments
✅ Financial juridiction, fiscal matters, taxation, legal finance
✅ Mathematical calculations, statistical analysis, algorithms
✅ Data analysis, visualization, patterns, trends, forecasting
✅ Basic greetings and polite conversation

RESTRICTED DOMAINS:
❌ Sports, entertainment, movies, music, celebrities
❌ Cooking, recipes, food, restaurants
❌ Travel, tourism, geography (unless economic)
❌ Technology (unless financial/analytical applications)
❌ Health, medicine, fitness
❌ Politics (unless economic policy)
❌ General knowledge, trivia, history (unless economic)
❌ Personal advice (unless financial)

IMPORTANT: Be strict in classification. If unsure, classify as RESTRICTED.

Respond with EXACTLY one word: either "ALLOWED" or "RESTRICTED"

Question to classify:"""

# Restriction response message
RESTRICTION_MESSAGE = """I'm specialized in financial and analytical domains. I can help you with:

🏦 **Banking & Finance**: Investments, portfolios, financial planning, banking services
📊 **Economic Analysis**: Market trends, economic indicators, fiscal policy
💰 **Fiscal & Legal**: Taxation, financial regulations, compliance matters  
🔢 **Mathematics & Statistics**: Calculations, statistical analysis, data modeling
📈 **Data Analysis**: Visualization, patterns, forecasting, analytical insights
👋 **General Conversation**: Greetings and polite interaction

Please ask me something related to these areas, and I'll be happy to help!"""

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