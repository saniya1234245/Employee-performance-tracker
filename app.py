from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Load datasets
general_data = pd.read_csv('datasets\general_data.csv')
manager_survey_data = pd.read_csv('datasets\manager_survey_data (1).csv')
employee_survey_data = pd.read_csv('datasets\employee_survey_data (1).csv')

@app.route('/')
def home():
    # Sample data for pie chart (attrition)
    # attrition_data = general_data['Attrition'].value_counts()
    # plt.figure(figsize=(6,6))
    # plt.pie(attrition_data, labels=attrition_data.index, autopct='%1.1f%%', startangle=90)
    # plt.savefig('static/charts/attrition_pie.png')
    return render_template('index.html', title='Home')

@app.route('/demographics')
def demographics():
    # Example graph: Age distribution histogram
    plt.figure(figsize=(10,6))
    sns.histplot(general_data['Age'], bins=20, kde=True)
    plt.title('Age Distribution of Employees')
    plt.savefig('static/charts/age_distribution.png')
    return render_template('demographics.html', title='Employee Demographics')

@app.route('/performance')
def performance():
    # Example graph: Job involvement vs Performance Rating
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=manager_survey_data['JobInvolvement'], y=manager_survey_data['PerformanceRating'])
    plt.title('Job Involvement vs Performance Rating')
    plt.savefig('static/charts/job_involvement_vs_performance.png')
    return render_template('performance.html', title='Performance Analysis')

@app.route('/satisfaction')
def satisfaction():
    # Example graph: Work-life balance vs Job Satisfaction
    plt.figure(figsize=(10,6))
    sns.barplot(x=employee_survey_data['WorkLifeBalance'], y=employee_survey_data['JobSatisfaction'])
    plt.title('Work-life Balance vs Job Satisfaction')
    plt.savefig('static/charts/work_life_vs_job_satisfaction.png')
    return render_template('satisfaction.html', title='Satisfaction & Work-Life Balance')

@app.route('/attrition')
def attrition():
    # Example graph: Monthly income by attrition
    plt.figure(figsize=(10,6))
    sns.boxplot(x=general_data['Attrition'], y=general_data['MonthlyIncome'])
    plt.title('Attrition vs Monthly Income')
    plt.savefig('static/charts/attrition_vs_income.png')
    return render_template('attrition.html', title='Attrition & Salary Insights')

if __name__ == '__main__':
    app.run(debug=True)
