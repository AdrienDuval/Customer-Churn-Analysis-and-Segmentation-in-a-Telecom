# Exam Requirements vs Current Project Structure

## Exam Requirements Analysis

### Required Components

| Requirement | Exam Specification | Current Status | Action Needed |
|------------|-------------------|----------------|---------------|
| **1. Problématique business** | Business context, dataset presentation, clear DS objective | ✅ README covers this | None |
| **2. EDA** | `eda.ipynb` with structure, stats, missing values, visualizations, correlations, outliers | ⚠️ `notebooks/01_eda.ipynb` exists but empty | Populate notebook |
| **3. Preprocessing** | Missing values, encoding, normalization with justification | ⚠️ `notebooks/02_preprocessing.ipynb` exists but empty | Populate notebook |
| **4. Modélisation** | 1 supervised + 1 unsupervised model with justification | ⚠️ `notebooks/03_modeling.ipynb` exists but empty | Implement both models |
| **5. Sauvegarde modèle** | Model saved as `.pkl` and reloadable | ❌ Missing | Save model as .pkl |
| **6. API** | Flask or FastAPI with `/predict` endpoint | ⚠️ `api/main.py` exists but empty | Implement API with /predict |
| **7. Déploiement (bonus)** | GitHub, README, Dockerfile | ⚠️ README ✅, GitHub ?, Dockerfile ❌ | Add Dockerfile |
| **8. Analyse business** | Business impact, limitations, perspectives | ✅ README covers this | None |

## Detailed Comparison

### ✅ What's Aligned

1. **Business Context**: README clearly explains Telecom/SaaS churn problem
2. **Dataset**: Telco Customer Churn dataset is appropriate
3. **Structure**: Good folder organization
4. **Requirements files**: Present for both root and API

### ⚠️ Critical Issues

#### 1. **Notebook Naming Discrepancy**
- **Exam expects**: `eda.ipynb` (in root?)
- **Current structure**: `notebooks/01_eda.ipynb`
- **Decision needed**: Keep numbered structure or create `eda.ipynb` in root?

#### 2. **Empty Notebooks**
All three notebooks are empty and need implementation:
- `01_eda.ipynb` - EDA with visualizations, correlations, outliers
- `02_preprocessing.ipynb` - Cleaning, encoding, normalization
- `03_modeling.ipynb` - Supervised + Unsupervised models

#### 3. **Model Persistence**
- **Exam requires**: `.pkl` format
- **Current**: No model saved yet
- **Action**: Save model as `.pkl` in `models/` folder

#### 4. **API Implementation**
- **Exam requires**: `/predict` endpoint (Flask or FastAPI)
- **Current**: `api/main.py` is empty
- **Action**: Implement FastAPI with `/predict` endpoint

#### 5. **Missing Bonus Components**
- Dockerfile (bonus +2 points)
- GitHub repository setup

## Barème Alignment (/20)

| Criterion | Points | Current Status | Notes |
|-----------|--------|----------------|-------|
| Problématique business | 2 | ✅ Ready | README covers this |
| Qualité EDA | 3 | ⚠️ Empty | Need to implement |
| Cleaning + preprocessing | 3 | ⚠️ Empty | Need to implement |
| Modèle supervisé | 3 | ⚠️ Empty | Need to implement |
| Modèle non supervisé | 2 | ⚠️ Empty | Need to implement |
| Métriques et interprétation | 2 | ⚠️ Empty | Need to implement |
| Modèle .pkl fonctionnel | 1 | ❌ Missing | Need to save model |
| API fonctionnelle | 3 | ⚠️ Empty | Need to implement |
| Analyse business | 1 | ✅ Ready | README covers this |
| Qualité globale | 1 | ⚠️ Partial | Structure good, content missing |
| **Bonus: Docker** | +2 | ❌ Missing | Optional but valuable |

## Required Deliverables Checklist

- [ ] `eda.ipynb` OR `notebooks/01_eda.ipynb` (populated)
- [x] `api/` folder (structure exists)
- [ ] `api/main.py` with `/predict` endpoint
- [ ] `model.pkl` (or `models/model.pkl`)
- [ ] README.md (✅ exists and comprehensive)
- [ ] GitHub repository (verify)
- [ ] Dockerfile (bonus)

## Specific Exam Requirements

### EDA Requirements (3 points)
- [ ] Data structure analysis
- [ ] Descriptive statistics
- [ ] Missing values analysis
- [ ] Visualizations
- [ ] Correlations
- [ ] Outliers detection
- [ ] Hypotheses formulation

### Preprocessing Requirements (3 points)
- [ ] Missing values handling (with justification)
- [ ] Encoding (with justification)
- [ ] Normalization if needed (with justification)
- [ ] Clear justification for each choice

### Modeling Requirements (5 points total)
**Supervised (3 points):**
- [ ] One supervised model implemented
- [ ] Algorithm justification
- [ ] Metrics evaluation
- [ ] Model interpretation

**Unsupervised (2 points):**
- [ ] One unsupervised model implemented
- [ ] Algorithm justification
- [ ] Results interpretation

### API Requirements (3 points)
- [ ] Flask OR FastAPI
- [ ] `/predict` endpoint
- [ ] Model loading from .pkl
- [ ] Functional and testable

### Model Persistence (1 point)
- [ ] Model saved as `.pkl`
- [ ] Model can be reloaded
- [ ] Works with API

## Recommendations

### Immediate Actions

1. **Decide on notebook naming**:
   - Option A: Keep `notebooks/01_eda.ipynb` (better organization)
   - Option B: Create `eda.ipynb` in root (matches exam exactly)
   - **Recommendation**: Keep numbered structure, but ensure it's clear in README

2. **Implement notebooks** in order:
   - Start with EDA
   - Then preprocessing
   - Finally modeling (both supervised and unsupervised)

3. **Save model as .pkl**:
   - Use `joblib` or `pickle` to save as `.pkl`
   - Save in `models/` folder
   - Test reloading

4. **Implement API**:
   - Use FastAPI (already in requirements)
   - Create `/predict` endpoint
   - Load model from `.pkl`
   - Add input validation (Pydantic)

5. **Add Dockerfile** (bonus):
   - Dockerfile for API
   - docker-compose.yml (optional)
   - .dockerignore

### Structure Recommendation

```
FinalProject/
├── data/
│   └── Telco_customer_churn.xlsx
├── notebooks/
│   ├── 01_eda.ipynb              ⚠️ To implement
│   ├── 02_preprocessing.ipynb    ⚠️ To implement
│   └── 03_modeling.ipynb         ⚠️ To implement
├── api/
│   ├── main.py                   ⚠️ To implement (/predict endpoint)
│   └── requirements.txt
├── models/
│   └── model.pkl                 ❌ To create
├── requirements.txt
├── readme.md                     ✅ Good
├── Dockerfile                    ❌ Bonus (to add)
└── .gitignore
```

## Next Steps Priority

1. **HIGH**: Populate `01_eda.ipynb` with comprehensive EDA
2. **HIGH**: Populate `02_preprocessing.ipynb` with cleaning and preprocessing
3. **HIGH**: Populate `03_modeling.ipynb` with both supervised and unsupervised models
4. **HIGH**: Save model as `.pkl` in `models/` folder
5. **HIGH**: Implement `api/main.py` with `/predict` endpoint
6. **MEDIUM**: Add Dockerfile for bonus points
7. **LOW**: Verify GitHub setup
