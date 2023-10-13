import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_analytics


with streamlit_analytics.track(save_to_json="web-analytics.json"):

    st.set_page_config(layout="wide")

    # Load the dataset
    @st.cache_data
    def load_data():
        data = pd.read_csv('events.csv')
        return data

    try:
        data = load_data()
    except OverflowError:
        st.error("Error: Data contains values larger than the maximum supported integer size in JavaScript (2^53). Please check your data.")

    # Set a title for your dashboard
    st.title('E-commerce Behavior Dashboard')

    # Sidebar for filtering options
    st.sidebar.subheader('Filter Data')

    # Filter out rows with missing or non-string values in the 'category_code' column
    data = data.dropna(subset=['category_code'])
    data = data[data['category_code'].apply(lambda x: isinstance(x, str))]

    # Get unique top-level categories
    top_level_categories = data['category_code'].apply(lambda x: x.split('.')[0]).unique()

    # Allow users to select the top-level category
    selected_top_level_category = st.sidebar.selectbox('Select Top-Level Category', [''] + list(top_level_categories))

    # Initialize variables for sub-level categories
    sub_level_categories = []
    selected_sub_level_category1 = ""
    selected_sub_level_category2 = ""

    if selected_top_level_category:
        # Get sub-level categories based on the selected top-level category
        sub_level_categories = data[data['category_code'].apply(lambda x: x.startswith(selected_top_level_category))]['category_code'].apply(lambda x: '.'.join(x.split('.')[1:2])).unique()
        # Allow users to select the first sub-level category
        selected_sub_level_category1 = st.sidebar.selectbox('Select First Sub-Level Category', [''] + list(sub_level_categories))

    if selected_sub_level_category1:
        # Get sub-level categories based on the selected top-level and first sub-level categories
        sub_level_categories2 = data[
            (data['category_code'].apply(lambda x: x.startswith(selected_top_level_category + '.' + selected_sub_level_category1)))
        ]['category_code'].apply(lambda x: '.'.join(x.split('.')[2:])).unique()

        if len(sub_level_categories2) > 0:
            # Allow users to select the second sub-level category
            selected_sub_level_category2 = st.sidebar.selectbox('Select Second Sub-Level Category', [''] + list(sub_level_categories2))

    # Check if any sub-level category is selected and filter data accordingly
    if selected_sub_level_category2:
        filtered_data = data[
            (data['category_code'].apply(lambda x: x.startswith(selected_top_level_category + '.' + selected_sub_level_category1 + '.' + selected_sub_level_category2)))
        ]
    elif selected_sub_level_category1:
        filtered_data = data[
            (data['category_code'].apply(lambda x: x.startswith(selected_top_level_category + '.' + selected_sub_level_category1)))
        ]
    elif selected_top_level_category:
        filtered_data = data[
            (data['category_code'].apply(lambda x: x.startswith(selected_top_level_category)))
        ]
    else:
        # If no filters are selected, show all data
        filtered_data = data

    purchase_data = filtered_data[filtered_data['event_type'] == 'purchase']
    # Filter data for 'view' events
    view_data = filtered_data[filtered_data['event_type'] == 'view']
    # Filter data for 'cart' events
    cart_data = filtered_data[filtered_data['event_type'] == 'cart']

    # Create a container for the most common brand and category
    brand_category_container = st.container()

    # Within the container, create a selectbox for event type
    with brand_category_container:
        event_type = st.selectbox('Select Event Type', ['purchase', 'view', 'cart'], index=0)

        # Determine the data based on the selected event type
        if event_type == 'purchase':
            selected_data = purchase_data
            event_title = 'Purchased Products'
        elif event_type == 'view':
            selected_data = view_data
            event_title = 'Viewed Products'
        else:
            selected_data = cart_data
            event_title = 'Products Added to Cart'

    # Display the most common brand and category for the selected event type
    if len(selected_data) > 0:
        if selected_sub_level_category2:
            event_title = selected_sub_level_category2.capitalize()
        elif selected_sub_level_category1:
            event_title = selected_sub_level_category1.capitalize()
        else:
            if selected_top_level_category:
                event_title = selected_top_level_category.capitalize()
            else:
                event_title = ""

        most_common_brand = selected_data['brand'].mode().iloc[0].capitalize()
        most_common_category = selected_data['category_code'].mode().iloc[0].split('.')[-1].capitalize()

        col1, col2 = st.columns(2)

        with col1:
            st.error(f"""
            #### Most Common Brand{f" for {event_title}" if event_title else ""}
            # {most_common_brand}
            """)

            # Create a single bar chart for the most common brands
            brand_counts = selected_data['brand'].value_counts().head(10)
            fig_brand = px.bar(
                x=brand_counts.index,
                y=brand_counts.values,
                labels={'x': 'Brand', 'y': 'Count'},
                title=f'Top 10 Most Common Brands for {event_title}',
            )
            st.plotly_chart(fig_brand)

        with col2:
            st.error(f"""
            #### Most Common Category{f" for {event_title}" if event_title else ""}
            # {most_common_category}
            """)

            # Create a single bar chart for the most common categories
            category_counts = selected_data['category_code'].apply(lambda x: x.split('.')[-1]).value_counts().head(10)
            fig_category = px.bar(
                x=category_counts.index,
                y=category_counts.values,
                labels={'x': 'Category', 'y': 'Count'},
                title=f'Top 10 Most Common Categories for {event_title}',
            )
            st.plotly_chart(fig_category)

    else:
        if selected_top_level_category:
            st.warning(f"No data available for the selected event type: {event_title.capitalize()}")
        else:
            st.warning("Please select a category to display results.")


    #### STOP

    # ... (previous code)

    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # ... (previous code)

    # Create a container for the entire layout
    with st.container():
        # Use columns for responsive columns
        col1, col2 = st.columns(2)

        # Column 1: PIE CHART (Stretches to full width)
        with col1:
            # Calculate statistics for 'viewed' events
            total_viewed_products = len(view_data)
            average_viewed_price = view_data['price'].mean()
            most_common_viewed_brand = view_data['brand'].mode().iloc[0]

            # Calculate statistics for 'added to cart' events
            total_cart_products = len(cart_data)
            average_cart_price = cart_data['price'].mean()
            most_common_cart_brand = cart_data['brand'].mode().iloc[0]

            # Calculate statistics for 'purchased' events
            total_purchased_products = len(purchase_data)
            average_purchased_price = purchase_data['price'].mean()
            most_common_purchased_brand = purchase_data['brand'].mode().iloc[0]

            # Create a summary table to compare the statistics
            summary_data = {
                'Event Type': ['Viewed', 'Added to Cart', 'Purchased'],
                'Total Products': [total_viewed_products, total_cart_products, total_purchased_products],
                'Average Price': [average_viewed_price, average_cart_price, average_purchased_price],
                'Most Common Brand': [most_common_viewed_brand, most_common_cart_brand, most_common_purchased_brand]
            }

            # Convert the summary data to a DataFrame
            summary_df = pd.DataFrame(summary_data)

            import plotly.express as px

            # Create a pie chart for the distribution of total products
            fig = px.pie(
                summary_df,
                values='Total Products',
                names='Event Type',
                title='Distribution of Total Products by Event Type'
            )

            # Set the width and height for the chart
            fig.update_layout(width=600, height=600)

            # Display the pie chart
            st.write("### Distribution of Total Products by Event Type")
            st.plotly_chart(fig)

        # Column 2: Category Analysis (Takes up default space)
        with col2:
            # Title for the analysis
            st.write("### Cart Additions vs. Successful Purchases")

            # Category-wise Analysis
            if len(filtered_data) > 0:
                # Create a bar chart to visualize the number of 'added to cart' and 'purchased' events for all categories
                if len(cart_data) > 0 or len(purchase_data) > 0:
                    category_event_counts = pd.DataFrame({
                        'Event Type': ['Added to Cart', 'Purchased'],
                        'Number of Events': [len(cart_data), len(purchase_data)]
                    })

                    fig_all_categories_events = px.bar(
                        category_event_counts,
                        x='Event Type',
                        y='Number of Events',
                        labels={'Event Type': 'Event Type', 'Number of Events': 'Number of Events'},
                    )

                    # Set the width and height for the chart
                    fig_all_categories_events.update_layout(width=600, height=600)

                    # Display the bar chart for all categories
                    st.plotly_chart(fig_all_categories_events)
                else:
                    st.info("No 'Added to Cart' or 'Purchased' events found for the selected filters.")
            else:
                st.warning("No data available for the selected filters.")


    # ... (previous code)

    # Brand Analysis: Explore the popularity of different brands within each category, and visualize brand preferences among users.
    st.write("## Brand Analysis")
    st.write("Explore the popularity of different brands within each category, and visualize brand preferences among users.")

    # Calculate brand popularity within each category
    if len(filtered_data) > 0:
        # Extract the subcategory from the 'category_code' column
        category_brand_counts = filtered_data.groupby(['category_code', 'brand']).size().reset_index(name='count')
        category_brand_counts['subcategory'] = category_brand_counts['category_code'].str.split('.').str[-1].str.capitalize()

        # Create a treemap to visualize brand preferences within each subcategory
        fig_brand_analysis = px.treemap(
            category_brand_counts,
            path=['subcategory', 'brand'],
            values='count',
            title='Brand Preferences Within Each Subcategory',
            labels={'subcategory': 'Subcategory', 'count': 'Count', 'brand': 'Brand'},
            hover_data={'count': False},  # Display count without hovering
        )

        # Set the font size, width, and height for the chart
        fig_brand_analysis.update_layout(
            font=dict(size=18),  # Increase font size
            width=1600,
            height=800,
        )

        # Display the brand analysis treemap
        st.plotly_chart(fig_brand_analysis)
    else:
        st.warning("No data available for the selected filters.")



    # ... (your existing code)
    # Convert the 'event_time' column to a datetime object
    data['event_time'] = pd.to_datetime(data['event_time'])

    # Extract the date and hour from the 'event_time' column
    data['event_date'] = data['event_time'].dt.date
    data['event_hour'] = data['event_time'].dt.hour

    # Create a container with two rows
    container = st.container()

    # Row 1: Daily and Hourly View Event Chart
    with container:
        row1 = st.columns(2)
        with row1[0]:
            # Daily Event Count for View
            daily_event_counts_view = data[data['event_type'] == 'view'].groupby(['event_date']).size().reset_index(name='count')
            daily_event_fig_view = px.line(daily_event_counts_view, x='event_date', y='count',
                labels={'count': 'Daily View Event Count', 'event_date': 'Date'}, title='Daily View Event Counts'
            )
            daily_event_fig_view.update_xaxes(title_text='Date')
            daily_event_fig_view.update_yaxes(title_text='Number of View Events')
            st.plotly_chart(daily_event_fig_view)

        with row1[1]:
            # Hourly Event Count for View
            hourly_event_counts_view = data[data['event_type'] == 'view'].groupby(['event_hour']).size().reset_index(name='count')
            hourly_event_fig_view = px.line(hourly_event_counts_view, x='event_hour', y='count',
                labels={'count': 'Hourly View Event Count', 'event_hour': 'Hour of the Day'}, title='Hourly View Event Counts'
            )
            hourly_event_fig_view.update_xaxes(title_text='Hour of the Day')
            hourly_event_fig_view.update_yaxes(title_text='Number of View Events')
            st.plotly_chart(hourly_event_fig_view)

    # Row 2: Daily and Hourly Added to Cart and Purchased Event Chart
    with container:
        row2 = st.columns(2)
        with row2[0]:
            # Daily Event Count for Added to Cart
            daily_event_counts_cart = data[data['event_type'] == 'cart'].groupby(['event_date']).size().reset_index(name='count')
            daily_event_counts_purchase = data[data['event_type'] == 'purchase'].groupby(['event_date']).size().reset_index(name='count')
            daily_event_counts_cart_purchase = daily_event_counts_cart.merge(
                daily_event_counts_purchase, on='event_date', suffixes=('_cart', '_purchase')
            )

            daily_event_fig_cart_purchase = px.line(daily_event_counts_cart_purchase, x='event_date', y=['count_cart', 'count_purchase'],
                labels={'count_cart': 'Daily Added to Cart Event Count', 'count_purchase': 'Daily Purchased Event Count', 'event_date': 'Date'},
                title='Daily Added to Cart and Purchased Event Counts'
            )
            daily_event_fig_cart_purchase.update_xaxes(title_text='Date')
            daily_event_fig_cart_purchase.update_yaxes(title_text='Number of Events')
            st.plotly_chart(daily_event_fig_cart_purchase)

        with row2[1]:
            # Hourly Event Count for Added to Cart
            hourly_event_counts_cart = data[data['event_type'] == 'cart'].groupby(['event_hour']).size().reset_index(name='count')
            hourly_event_counts_purchase = data[data['event_type'] == 'purchase'].groupby(['event_hour']).size().reset_index(name='count')
            hourly_event_counts_cart_purchase = hourly_event_counts_cart.merge(
                hourly_event_counts_purchase, on='event_hour', suffixes=('_cart', '_purchase')
            )

            hourly_event_fig_cart_purchase = px.line(hourly_event_counts_cart_purchase, x='event_hour', y=['count_cart', 'count_purchase'],
                labels={'count_cart': 'Hourly Added to Cart Event Count', 'count_purchase': 'Hourly Purchased Event Count', 'event_hour': 'Hour of the Day'},
                title='Hourly Added to Cart and Purchased Event Counts'
            )
            hourly_event_fig_cart_purchase.update_xaxes(title_text='Hour of the Day')
            hourly_event_fig_cart_purchase.update_yaxes(title_text='Number of Events')
            st.plotly_chart(hourly_event_fig_cart_purchase)

    # ... (your existing code)