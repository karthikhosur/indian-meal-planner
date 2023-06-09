import streamlit as st
import pandas as pd
import random

# Function to filter the DataFrame based on selected cuisines, courses, and diets


def filter_data(df, selected_cuisines, selected_courses, selected_diets):
    filtered_df = df[(df['Cuisine'].isin(selected_cuisines))
                     & (df['Course'].isin(selected_courses))
                     & (df['Diet'].isin(selected_diets))]
    return filtered_df

# Function to get a random recipe from the filtered DataFrame


def get_random_recipe(filtered_df):
    random_recipe = random.choice(filtered_df['RecipeName'].values)
    recipe_info = filtered_df[filtered_df['RecipeName']
                              == random_recipe].iloc[0]
    recipe_url = recipe_info['URL']
    return random_recipe, recipe_info, recipe_url

# Function to get the previous recipe in the filtered DataFrame


def get_prev_recipe(filtered_df, random_recipe):
    prev_recipe = filtered_df[filtered_df['RecipeName'] < random_recipe].sort_values(
        'RecipeName').iloc[-1]['RecipeName']
    recipe_info = filtered_df[filtered_df['RecipeName'] == prev_recipe].iloc[0]
    recipe_url = recipe_info['URL']
    return prev_recipe, recipe_info, recipe_url

# Function to get the next recipe in the filtered DataFrame


def get_next_recipe(filtered_df, random_recipe):
    next_recipe = filtered_df[filtered_df['RecipeName'] > random_recipe].sort_values(
        'RecipeName').iloc[0]['RecipeName']
    recipe_info = filtered_df[filtered_df['RecipeName'] == next_recipe].iloc[0]
    recipe_url = recipe_info['URL']
    return next_recipe, recipe_info, recipe_url


# Load CSV file
df = pd.read_csv('IndianFoodDataset.csv')

# Get unique values in 'Cuisine', 'Course', and 'Diet' columns
unique_cuisines = df['Cuisine'].unique()
unique_courses = df['Course'].unique()
unique_diets = df['Diet'].unique()

# Create multiselect widgets
selected_cuisines = st.sidebar.multiselect('Select Cuisines', unique_cuisines)
selected_courses = st.sidebar.multiselect('Select Courses', unique_courses)
selected_diets = st.sidebar.multiselect('Select Diets', unique_diets)

# Filter the DataFrame based on the selected values
filtered_df = filter_data(df, selected_cuisines,
                          selected_courses, selected_diets)

# Get a random recipe
random_recipe, recipe_info, recipe_url = get_random_recipe(filtered_df)

# Add a title for the recipe
st.title("🍽️ Recipe Information")

# Display the recipe name with a custom font size and weight
st.markdown(
    f"<h2 style='font-weight: bold;'>{random_recipe}</h2>", unsafe_allow_html=True)

# Format and display the ingredients list
st.subheader("Ingredients")
# ingredients_list = ', '.join(
#     [f"{ingredient}" for ingredient in recipe_info['Ingredients']])
# ingredients_list = recipe_info['Ingredients'].split(',')

st.subheader("Ingredients")
ingredients_list = recipe_info['Ingredients'].split(',')

st.write('\n'.join([f"- {ingredient}" for ingredient in ingredients_list]))
# Display diet, cook time, and prep time in a nicely formatted way
st.subheader("Details")
st.markdown(f"""
<style>
    .details {{
        display: flex;
        justify-content: space-between;
    }}
    .detail {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .detail-title {{
        font-weight: bold;
    }}
</style>

<div class="details">
    <div class="detail">
        <span class="detail-title">Diet</span>
        <span>{recipe_info['Diet']}</span>
    </div>
    <div class="detail">
        <span class="detail-title">Cook Time (mins)</span>
        <span>{recipe_info['CookTimeInMins']}</span>
    </div>
    <div class="detail">
        <span class="detail-title">Prep Time (mins)</span>
        <span>{recipe_info['PrepTimeInMins']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Add buttons for navigation and redirecting to URL
prev_button, next_button = st.columns(2)

if prev_button.button('Previous Recipe'):
    # Get previous recipe in filtered DataFrame
    prev_recipe, recipe_info, recipe_url = get_prev_recipe(
        filtered_df, random_recipe)
    random_recipe = prev_recipe
    # Enable "Next Recipe" button
    next_button.empty()

elif next_button.button('Next Recipe') and len(filtered_df) > 1:
    # Get next recipe in filtered DataFrame
    next_recipe, recipe_info, recipe_url = get_next_recipe

# Display the recipe URL again
st.markdown(
    f"<a href='{recipe_url}'>View recipe source</a>", unsafe_allow_html=True)
