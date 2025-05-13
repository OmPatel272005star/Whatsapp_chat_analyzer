import re
import pandas as pd
def preprocess(data):
    pattern = r"(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?(?:am|pm)) - ([^:]+): (.+)"
    matches = re.findall(pattern, data)

    # Extract into two lists
    dates = []
    messages = []

    for match in matches:
        date_time, name, message = match
        dates.append(date_time)
        messages.append(f"{name}: {message}")

    dates = [dt.replace(',', '').replace('\u202f', '') for dt in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y %I:%M%p')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if (entry[1:]):
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            message.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num']= df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df