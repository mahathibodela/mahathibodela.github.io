
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import os 


def get_leetcode_stats(username):
    url = 'https://leetcode.com/graphql'
    query = """
    query getUserProfile($username: String!) {
        allQuestionsCount {
            difficulty
            count
        }
        userContestRanking(username: $username) {
            attendedContestsCount
            rating
            globalRanking
            totalParticipants
            topPercentage
            badge {
                name
            }
        }
        matchedUser(username: $username) {
            username
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
        }
    }
    """
    variables = {
        "username": username
    }
    payload = {
        "query": query,
        "variables": variables
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    # print(response.json())
    return response.json()

def load_json_file(filename,data_set):
    with open(filename, 'r') as json_file:
        stats = json.load(json_file)['data']['matchedUser']['submitStats']['acSubmissionNum']
    print(filename)
    for st in stats:
        if st['difficulty'] in data_set:
            data_set[st['difficulty']]['solved'] = st['count']
    with open(filename, 'r') as json_file:
        stats = json.load(json_file)['data']
    for st in stats["allQuestionsCount"]:
        if st['difficulty'] in data_set:
            data_set[st['difficulty']]['total'] = st['count']
    data_set['contests'] = stats['userContestRanking']['attendedContestsCount']
    data_set['rating'] = int(stats['userContestRanking']['rating'])
    data_set['top_percentage'] = float(f'{stats['userContestRanking']['topPercentage']:.2f}')

def generate_pie_chart(stats):
    leetcode_data = {
        "Easy": {"solved": 0, "total": 0},
        "Medium": {"solved": 0, "total": 0},
        "Hard": {"solved": 0, "total": 0},
        "contests": 0,
        "rating": 0,
        "top_percentage": 0
    }
    load_json_file('docs/leetcode_stats.json',leetcode_data)
    # Calculate total solved and total problems
    total_solved = sum([leetcode_data[difficulty]["solved"] for difficulty in ["Easy", "Medium", "Hard"]])
    total_problems = sum([leetcode_data[difficulty]["total"] for difficulty in ["Easy", "Medium", "Hard"]])

    # Define the data for the pie chart
    labels = ['Easy', 'Medium', 'Hard']
    sizes = [leetcode_data[label]["solved"] for label in labels]
    total_sizes = [leetcode_data[label]["total"] for label in labels]
    colors = ['#4CAF50', '#FFC107', '#F44336']

    # Create the pie chart
    fig, ax = plt.subplots()

    wedges, texts = ax.pie(
        sizes, labels=None, colors=colors, autopct=None,
        startangle=90, wedgeprops=dict(width=0.3, edgecolor='w')
    )

    # Draw center circle for the donut chart effect
    centre_circle = plt.Circle((0,0),0.70,fc='black')
    fig.gca().add_artist(centre_circle)

    # Draw the text in the center
    ax.text(0, 0, f'{total_solved}\n____\n\n{total_problems}', color='white', ha='center', va='center', fontsize=14)

    # Add text labels manually
    for i, (wedge, label) in enumerate(zip(wedges, labels)):
        ang = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        ax.annotate(f'{label} {sizes[i]}/{total_sizes[i]}', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, color='black', weight='bold', fontsize=12,
                    arrowprops=dict(arrowstyle="-", color='black', connectionstyle=connectionstyle))

    # Add additional information
    plt.text(1.5, 1, f"Contests: {leetcode_data['contests']}", fontsize=12, color='black')
    plt.text(1.5, 0.8, f"Rating: {leetcode_data['rating']}", fontsize=12, color='black')
    plt.text(1.5, 0.6, f"Top %: {leetcode_data['top_percentage']}%", fontsize=12, color='black')

    # Set background color
    fig.patch.set_facecolor('white')

    # Save the figure
    plt.savefig('docs/leetcode.png', bbox_inches='tight', facecolor='white')

    # # Display the plot
    # plt.show()


def save_json_to_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


username = 'mahathibodela7'
stats = get_leetcode_stats(username)
save_json_to_file(stats, 'docs/leetcode_stats.json')
generate_pie_chart(stats)

