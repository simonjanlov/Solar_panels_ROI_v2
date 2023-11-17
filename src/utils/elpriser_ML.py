import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv("final_project\data\elpriser_sverige96-23.csv")  

# # List of columns to increase by 25% (skatt)
# columns_to_increase = ['Lägenhet', 'Villa utan elvärme', 'Villa med elvärme', 'Större hushåll', 'Näringsverksamhet', 'Småindustri']

# # Add 25% to the specified columns
# data[columns_to_increase] = data[columns_to_increase] * 1.25

# Select the columns of interest
data = data[["Year", "Villa utan elvärme"]]

# Split the data into features (X) and the target (y)
X = data[["Year"]]
y = data["Villa utan elvärme"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create polynomial features
degree = 2  
poly = PolynomialFeatures(degree=degree)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Create a linear regression model
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train_poly, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test_poly)

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)

# Calculate R-squared (R²)
r2 = r2_score(y_test, y_pred)

# Visualize the results (optional)
x_values = np.arange(1996, 2044, 1)
x_values_poly = poly.transform(x_values.reshape(-1, 1))
y_values_poly = model.predict(x_values_poly)

plt.scatter(X_test, y_test, color='blue', label='Actual Data')
plt.plot(x_values, y_values_poly, color='red', linewidth=2, label=f'Polynomial Regression (Degree {degree})')
plt.xlabel("Year")
plt.ylabel("Villa utan elvärme")
plt.legend()
plt.show()

# Now, you can use the model to make predictions for any given year
year_to_predict = 2024
year_to_predict_poly = poly.transform([[year_to_predict]])
predicted_value = model.predict(year_to_predict_poly)
print(f"Predicted kWh price {year_to_predict}: {predicted_value[0]}")

# Create a list of future years for prediction
future_years = [2024 + i for i in range(1, 21)]  # Predict for the next 20 years
future_years_poly = poly.transform(np.array(future_years).reshape(-1, 1))

# Predict 'Villa utan elvärme' values for each future year
future_predictions = model.predict(future_years_poly)

# Create a DataFrame to store the predictions
predictions_df = pd.DataFrame({'Year': future_years, 'Predicted kWh price': future_predictions})

# Display the predictions
print(predictions_df)
predictions_df.to_csv("predicted_prices.csv", index=False)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R²): {r2}")
