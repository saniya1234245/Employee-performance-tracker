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
    performance_counts = manager_survey_data.groupby('PerformanceRating')['EmployeeID'].count().reset_index()
    performance_counts.columns = ['PerformanceRating', 'Number of Employees']

    # graph: Job involvement vs Performance Rating
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=manager_survey_data['JobInvolvement'], y=manager_survey_data['PerformanceRating'])
    plt.title('Job Involvement vs Performance Rating')
    plt.savefig('static/charts/job_involvement_vs_performance.png')

    # graph: performance rating distribution
    plt.figure(figsize=(8, 6))
    sns.barplot(x='PerformanceRating', y='Number of Employees', data=performance_counts, palette='Blues_d')
    plt.title('Performance Rating Distribution')
    plt.xlabel('Performance Rating')
    plt.ylabel('Number of Employees')
    plt.savefig('static/charts/performance_rating_chart.png') 

    #graph: job onvolvement overview
    job_involvement_distribution = manager_survey_data.groupby('JobInvolvement')['EmployeeID'].count().reset_index()
    job_involvement_distribution.columns = ['JobInvolvement', 'EmployeeCount']
    plt.figure(figsize=(8, 8))
    plt.pie(
        job_involvement_distribution['EmployeeCount'], 
        labels=job_involvement_distribution['JobInvolvement'], 
        autopct='%1.1f%%', 
        colors=plt.cm.Oranges(range(0, 256, 64)),  # Optional: Orange color palette
        startangle=140
    )
    plt.title('Job Involvement Distribution', fontsize=16)
    plt.savefig('static/charts/jobInvolvement_overview.png') 

    return render_template('performance.html', graphs=['job_involvement_vs_performance.png', 'performance_rating_chart.png','jobInvovlement_overview.png'])

@app.route('/satisfaction')
def satisfaction():

    employee_survey_data = pd.read_csv('datasets\employee_survey_data (1).csv')
    general_data = pd.read_csv('datasets\general_data.csv')

    # Merge the datasets on EmployeeID
    merged_data = pd.merge(employee_survey_data, general_data, on='EmployeeID')

    # Group by YearsAtCompany and calculate average JobSatisfaction
    job_satisfaction_over_years = merged_data.groupby('YearsAtCompany')['JobSatisfaction'].mean().reset_index()

    # Group by Department and calculate average WorkLifeBalance
    work_life_balance_by_department = merged_data.groupby('Department')['WorkLifeBalance'].mean().reset_index()

    # graph: Work-life balance vs Job Satisfaction
    plt.figure(figsize=(10,6))
    sns.barplot(x=employee_survey_data['WorkLifeBalance'], y=employee_survey_data['JobSatisfaction'])
    plt.title('Work-life Balance vs Job Satisfaction')
    plt.savefig('static/charts/work_life_vs_job_satisfaction.png')

    # graph: Job satisfaction over years at company
    plt.figure(figsize=(10, 6))
    plt.plot(job_satisfaction_over_years['YearsAtCompany'], job_satisfaction_over_years['JobSatisfaction'], marker='o', linestyle='-', color='orange')
    plt.title('Job Satisfaction Over Time', fontsize=16)
    plt.xlabel('Years at Company', fontsize=14)
    plt.ylabel('Average Job Satisfaction Level (%)', fontsize=14)
    plt.xticks(job_satisfaction_over_years['YearsAtCompany'])
    plt.grid()
    plt.savefig('static/charts/job_satisfaction_over_time.png')

    #graph: work life balance satisfaction overview
    plt.figure(figsize=(10, 6))
    plt.bar(work_life_balance_by_department['Department'], work_life_balance_by_department['WorkLifeBalance'], color='orange')

    # Adding titles and labels
    plt.title('Work-Life Balance Satisfaction by Department', fontsize=16)
    plt.xlabel('Department', fontsize=14)
    plt.ylabel('Average Work-Life Balance Satisfaction Level (%)', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.savefig('static/charts/work_life_balance_department_comparison.png')
    plt.close()

    return render_template('satisfaction.html', graphs=['work_life_vs_job_satisfaction.png, job_satisfaction_over_time.png, work_life_balance_department_comparison.png'])

@app.route('/attrition')
def attrition():

    employee_data = pd.read_csv('datasets\general_data.csv')

    if employee_data['Attrition'].dtype == 'object':
        employee_data['Attrition'] = employee_data['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)


    # graph: Monthly income by attrition
    plt.figure(figsize=(10,6))
    sns.boxplot(x=general_data['Attrition'], y=general_data['MonthlyIncome'])
    plt.title('Attrition vs Monthly Income')
    plt.savefig('static/charts/attrition_vs_income.png')

    # graph: Salary Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(employee_data['MonthlyIncome'], bins=20, color='orange', edgecolor='black')
    plt.title('Salary Distribution Among Employees', fontsize=16)
    plt.xlabel('Salary', fontsize=14)
    plt.ylabel('Number of Employees', fontsize=14)
    plt.grid(axis='y')
    plt.savefig('static/charts/salary_distribution.png')

    #graph: attrition overview
    attrition_rates = employee_data.groupby('YearsAtCompany')['Attrition'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(attrition_rates['YearsAtCompany'], attrition_rates['Attrition'], marker='o', color='orange')
    plt.title('Attrition Rate Over Time', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Attrition Rate (%)', fontsize=14)
    plt.grid()
    plt.savefig('static/charts/attrition_rate_over_time.png')

    return render_template('attrition.html', graphs=['salary_distribution.png', 'attrition_vs_income.png', 'attrition_rate_over_time.png'])

if __name__ == '__main__':
    app.run(debug=True)
