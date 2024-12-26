import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def generate_sample_data(num_records=1000):
    """Generate sample credit data for demonstration"""
    np.random.seed(42)
    
    data = {
        'customer_id': range(1, num_records + 1),
        'age': np.random.randint(20, 70, num_records),
        'income': np.random.normal(60000, 20000, num_records),
        'credit_score': np.random.normal(700, 100, num_records),
        'loan_amount': np.random.normal(30000, 10000, num_records),
        'payment_history': np.random.uniform(0, 100, num_records),
        'existing_loans': np.random.randint(0, 5, num_records),
        'employment_length': np.random.randint(0, 30, num_records),
        'default_risk': np.random.uniform(0, 100, num_records)
    }
    
    # Clean up the data
    df = pd.DataFrame(data)
    df['income'] = df['income'].clip(20000, 150000)
    df['credit_score'] = df['credit_score'].clip(300, 850).astype(int)
    df['default_risk'] = df['default_risk'].clip(0, 100)
    
    return df

def calculate_risk_metrics(df):
    """Calculate key risk metrics from the data"""
    metrics = {
        'avg_credit_score': df['credit_score'].mean(),
        'high_risk_customers': len(df[df['default_risk'] > 70]),
        'total_loan_amount': df['loan_amount'].sum(),
        'avg_default_risk': df['default_risk'].mean()
    }
    return metrics

def create_dashboard():
    """Create the main dashboard application"""
    st.set_page_config(page_title="Credit Risk Insights Dashboard", layout="wide")
    
    # Title and description
    st.title("Credit Risk Insights Dashboard")
    st.markdown("Analysis of credit portfolio risk metrics and customer insights")
    
    # Generate sample data
    df = generate_sample_data()
    
    # Calculate metrics
    metrics = calculate_risk_metrics(df)
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Credit Score", f"{metrics['avg_credit_score']:.0f}")
    with col2:
        st.metric("High Risk Customers", metrics['high_risk_customers'])
    with col3:
        st.metric("Total Loan Amount", f"${metrics['total_loan_amount']:,.0f}")
    with col4:
        st.metric("Average Default Risk", f"{metrics['avg_default_risk']:.1f}%")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Credit Score Distribution
        fig_credit_score = px.histogram(
            df, 
            x='credit_score',
            title='Credit Score Distribution',
            nbins=30,
            color_discrete_sequence=['#3366cc']
        )
        st.plotly_chart(fig_credit_score, use_container_width=True)
        
        # Risk vs Income Scatter Plot
        fig_risk_income = px.scatter(
            df,
            x='income',
            y='default_risk',
            title='Default Risk vs Income',
            color='credit_score',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_risk_income, use_container_width=True)
    
    with col2:
        # Default Risk by Age Group
        df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], 
                                labels=['18-25', '26-35', '36-45', '46-55', '55+'])
        fig_age_risk = px.box(
            df,
            x='age_group',
            y='default_risk',
            title='Default Risk by Age Group'
        )
        st.plotly_chart(fig_age_risk, use_container_width=True)
        
        # Loan Amount vs Employment Length
        fig_loan_emp = px.scatter(
            df,
            x='employment_length',
            y='loan_amount',
            title='Loan Amount vs Employment Length',
            color='default_risk',
            color_continuous_scale='reds'
        )
        st.plotly_chart(fig_loan_emp, use_container_width=True)
    
    # Risk Distribution Table
    st.subheader("Risk Distribution Analysis")
    risk_bands = pd.cut(df['default_risk'], 
                       bins=[0, 20, 40, 60, 80, 100],
                       labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    risk_distribution = pd.DataFrame(risk_bands.value_counts()).reset_index()
    risk_distribution.columns = ['Risk Band', 'Number of Customers']
    st.dataframe(risk_distribution, use_container_width=True)
    
    # Add filters in the sidebar
    st.sidebar.header("Filters")
    min_credit_score = st.sidebar.slider("Minimum Credit Score", 300, 850, 300)
    max_default_risk = st.sidebar.slider("Maximum Default Risk", 0, 100, 100)
    
    # Filter the data
    filtered_df = df[
        (df['credit_score'] >= min_credit_score) &
        (df['default_risk'] <= max_default_risk)
    ]
    
    # Show filtered customer details
    st.subheader("Customer Details")
    st.dataframe(filtered_df[['customer_id', 'credit_score', 'income', 
                             'default_risk', 'loan_amount']].head(10))

if __name__ == "__main__":
    create_dashboard()