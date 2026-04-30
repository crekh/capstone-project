import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# -------------------------
# DATA AGENT
# -------------------------
class DataAgent:
    def load_data(self, path="cardio_train.csv"):
        import os

        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, path)

        df = pd.read_csv(full_path)
        return df

# -------------------------
# FEATURE AGENT
# -------------------------
class FeatureAgent:
    def process(self, df):
        df = df.copy()

        # Feature Engineering
        df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)

        df = df.dropna()

        return df


# -------------------------
# MODEL AGENT
# -------------------------
class ModelAgent:
    def train(self, df):
        features = [
            'age', 'gender', 'BMI', 'ap_hi', 'ap_lo',
            'cholesterol', 'gluc', 'smoke', 'alco', 'active'
        ]

        X = df[features]
        y = df["cardio"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        print(f"Model Accuracy: {acc:.4f}")

        return model, X


# -------------------------
# INSIGHT AGENT
# -------------------------
class InsightAgent:
    def generate(self, model, X):
        importance = pd.DataFrame({
            "feature": X.columns,
            "importance": model.feature_importances_
        }).sort_values(by="importance", ascending=False)

        return importance


# -------------------------
# PIPELINE CONTROLLER (FIXED)
# -------------------------
class PipelineController:
    def __init__(self):
        self.data_agent = DataAgent()
        self.feature_agent = FeatureAgent()
        self.model_agent = ModelAgent()
        self.insight_agent = InsightAgent()

    def run(self):
        # Step 1: Load data
        df = self.data_agent.load_data()

        # Step 2: Feature engineering
        df = self.feature_agent.process(df)

        # Step 3: Train model
        model, X = self.model_agent.train(df)

        # Step 4: Generate insights
        insights = self.insight_agent.generate(model, X)

        return model, insights