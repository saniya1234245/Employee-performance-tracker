from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load datasets
df_performance = pd.read_csv('datasets\manager_survey_data (1).csv')  # Dataset with 'PerformanceRating'
df_department = pd.read_csv('datasets\general_data.csv')    # Dataset with 'Department'
df_comparative = pd.read_csv('datasets\employee_survey_data (1).csv')  # Comparative dataset

# Home Page Route
@app.route('/')
def home():
    features = [
        {"title": "AI-Powered Analytics", "description": "Leverage cutting-edge AI to uncover hidden patterns and opportunities in your team's performance data.", "icon": "ai-icon.png"},
        {"title": "Real-time Collaboration", "description": "Foster teamwork with real-time updates and collaborative goal-setting features.", "icon": "collaboration-icon.png"},
        {"title": "Customizable Dashboards", "description": "Create personalized views that focus on the metrics that matter most to your organization.", "icon": "dashboard-icon.png"}
    ]
    
    testimonials = [
        {
            "quote": "This tool has revolutionized how we manage our team's performance. The insights we've gained have directly contributed to a 30% increase in productivity.",
            "author": "Jane Doe",
            "position": "CEO, TechCorp",
            "image": "jane-doe.jpg"
        },
        {
            "quote": "The intuitive interface and powerful analytics have made it easier than ever to identify and nurture top talent within our organization.",
            "author": "John Smith",
            "position": "HR Director, InnovateCo",
            "image": "john-smith.jpg"
        }
    ]
    return render_template('index.html')

# Analysis 1 Page
@app.route('/performance')
def performance():
    # Scatter plot for Performance Ratings
    scatter_fig = px.scatter(df_performance, x='EmployeeID', y='PerformanceRating',
                             title="Employee Performance Ratings", color='PerformanceRating')

    scatter_plot = pio.to_html(scatter_fig, full_html=False)
    return render_template('performance.html', scatter_plot=scatter_plot)

# Analysis 2 Page
@app.route('/department')
def department():
    # Bar plot for Departmental Distribution
    bar_fig = px.bar(df_department['Department'].value_counts().reset_index(),
                     x='index', y='Department', title="Department Distribution")

    bar_plot = pio.to_html(bar_fig, full_html=False)
    return render_template('department.html', bar_plot=bar_plot)

# Comparative Analysis Page
@app.route('/comparative')
def comparative():
    # Merging datasets for comparative analysis
    merged_df = pd.merge(df_performance, df_department, on='EmployeeID', how='inner')

    # Scatter Plot - Performance vs Department
    scatter_fig = px.scatter(merged_df, x='Department', y='PerformanceRating', color='Department',
                             title='Performance by Department')

    # Bar Plot - Average Performance per Department
    bar_fig = px.bar(merged_df.groupby('Department')['PerformanceRating'].mean().reset_index(),
                     x='Department', y='PerformanceRating', title='Average Performance per Department')

    # Histogram - Distribution of Performance Ratings
    hist_fig = px.histogram(merged_df, x='PerformanceRating', nbins=10, title='Distribution of Performance Ratings')

    scatter_plot = pio.to_html(scatter_fig, full_html=False)
    bar_plot = pio.to_html(bar_fig, full_html=False)
    hist_plot = pio.to_html(hist_fig, full_html=False)

    return render_template('comparative.html', scatter_plot=scatter_plot, bar_plot=bar_plot, hist_plot=hist_plot)

if __name__ == '__main__':
    app.run(debug=True)
