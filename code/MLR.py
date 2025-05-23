import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np

# Load the data
file_path = 'C:\\Users\\_'
df = pd.read_excel(file_path)

# Extract features and target
X = df[['CL=F', 'USO', 'GSCI index']]
y = df['Weekly U.S. Ending Stocks excluding SPR of Crude Oil  (Thousand Barrels)']
# Save feature names
feature_names = X.columns.tolist()
# Normalize the features and target variable
scaler_X = MinMaxScaler()
X_normalized = scaler_X.fit_transform(X)

scaler_y = MinMaxScaler()
y_normalized = scaler_y.fit_transform(y.values.reshape(-1, 1))

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_normalized, test_size=0.2, random_state=42)

# Add a constant for the MLR model
X_train_const = sm.add_constant(X_train)
X_test_const = sm.add_constant(X_test)

# Fit the MLR model
model = sm.OLS(y_train, X_train_const)
results = model.fit()
coefficients = results.params[1:]  # Exclude the intercept
variable_names = feature_names

# Find the variable with the highest absolute coefficient
most_important_variable = variable_names[np.argmax(np.abs(coefficients))]

print("The most important variable is:", most_important_variable)
# Print the summary of the MLR model
print(results.summary())

# Make predictions using the MLR model
y_pred = results.predict(X_test_const)

# Inverse transform predictions to the original scale for plotting
y_pred_original_scale = scaler_y.inverse_transform(y_pred.reshape(-1, 1))

# Inverse transform test target variable for plotting
y_test_original_scale = scaler_y.inverse_transform(y_test)

# Calculate Mean Squared Error (MSE) and R-squared
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print prediction and evaluation results
print(f'\nMean Squared Error: {mse:.2f}')
print(f'R-squared: {r2:.2f}')

# Calculate linear fit coefficients
fit_coefficients = np.polyfit(y_test_original_scale.flatten(), y_pred_original_scale.flatten(), 1)

# Generate linear fit line
fit_line = np.poly1d(fit_coefficients)

# Plot the regression results (optional)
plt.figure(figsize=(10, 6))
plt.scatter(y_test_original_scale, y_test_original_scale, color='gray', label='True Values')  # True values in red
plt.scatter(y_test_original_scale, y_pred_original_scale, color='black', label='Predicted Values')  # Predicted values in blue
plt.plot(y_test_original_scale, fit_line(y_test_original_scale), color='black', label='Linear Fit Line')
plt.title('Regression Results')
plt.xlabel('True Values (Thousand Barrels)')
plt.ylabel('Predicted Values (Thousand Barrels)')
plt.legend()
plt.show()

# Calculate Mean Absolute Percentage Error (MAPE)
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Calculate MAPE
mape = mean_absolute_percentage_error(y_test_original_scale, y_pred_original_scale)

# Print MAPE
print(f'Mean Absolute Percentage Error (MAPE): {mape:.4f}%')
