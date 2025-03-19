import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# ------------------- 1️⃣ Load Data -------------------
file_path = "/Users/prakashthapa/PycharmProject/new_project/Events.csv"  # Update this!
df = pd.read_csv(file_path)

# ------------------- 2️⃣ Inspect Initial Data -------------------
print("🔍 Initial Data Overview:")
print(df.head())  # Print first few rows for inspection
print("\nData Info (including datatypes):")
print(df.info())  # Check data types and missing values

# ------------------- 3️⃣ Data Cleaning -------------------
df.replace(["-", "?", "N/A", "n/a", "unknown", "no data"], np.nan, inplace=True)

# Check if any column is completely empty
empty_columns = df.columns[df.isna().all()]
if len(empty_columns) > 0:
    print(f"⚠️ These columns are completely empty and will be removed: {empty_columns}")

# Convert time strings (HH:MM:SS) to seconds (only apply to time columns)
def time_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except Exception as e:
        print(f"Error converting time: {e}")  # Log errors for invalid time formats
        return np.nan  # If conversion fails, return NaN

# List of columns that might have time data
time_columns = ["Resource Deployment Time", "Triage Time", "OT Preparation Time", "ICU Transfer Time"]
for col in time_columns:
    if col in df.columns:
        print(f"Converting {col} to seconds...")
        df[col] = df[col].astype(str).apply(time_to_seconds)

# Convert numeric columns (force conversion)
df = df.apply(pd.to_numeric, errors='coerce')

# ------------------- 4️⃣ Inspect Data After Cleaning -------------------
print("\n🔍 Data After Cleaning (first few rows):")
print(df.head())

# ------------------- 5️⃣ Visualize Missing Data Before Cleaning -------------------
plt.figure(figsize=(10, 6))
sns.heatmap(df.isna(), cbar=False, cmap="viridis")
plt.title("Missing Data Before Imputation")
plt.show()

# ------------------- 6️⃣ Handle Missing Values Properly -------------------
# Check for missing values
missing_values = df.isna().sum()
print("\n🔍 Missing Values Before Imputation:\n", missing_values[missing_values > 0])

# Remove columns that have all NaN values
df_cleaned = df.dropna(axis=1, how='all')

# Check if there are any valid columns left
if df_cleaned.shape[1] == 0:
    print("⚠️ No valid columns left after removing columns with all NaN values!")
else:
    # Use SimpleImputer to replace NaNs with column mean for remaining columns
    imputer = SimpleImputer(strategy="mean")
    df_imputed = pd.DataFrame(imputer.fit_transform(df_cleaned), columns=df_cleaned.columns)

    # ------------------- 7️⃣ Visualize Missing Data After Imputation -------------------
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_imputed.isna(), cbar=False, cmap="viridis")
    plt.title("Missing Data After Imputation")
    plt.show()

    # Verify no more NaNs
    print("\n✅ Missing Values After Imputation:\n", df_imputed.isna().sum().sum())  # Should print 0

# ------------------- 8️⃣ PCA After Fixing NaNs -------------------
# Proceed with PCA if we have valid imputed data
if df_cleaned.shape[1] > 0:
    features = [col for col in df_imputed.columns if col != 'HICS Activation Event']

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_imputed[features])  # No NaNs here now!

    pca = PCA()
    pca.fit(df_scaled)

    # Plot cumulative variance explained
    plt.figure(figsize=(10, 6))
    plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o', linestyle='--', color='b')
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("PCA: Cumulative Variance Explained")
    plt.grid(True)
    plt.show()

# ------------------- 9️⃣ Save Cleaned Data -------------------
# Save cleaned data only if we have valid imputed data
if df_cleaned.shape[1] > 0:
    df_imputed.to_csv("cleaned_data.csv", index=False)
    print("\n✅ Data cleaning and PCA analysis completed! Results saved as 'cleaned_data.csv'.")
else:
    print("⚠️ No valid columns to save after cleaning!")
