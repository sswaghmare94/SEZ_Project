import matplotlib.pyplot as plt
import numpy as np
import random
from flask import Flask, jsonify, request, json
from PIL import Image
import io
import base64
import flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

user_input_json_sample = {
    "project_name": "SIDG",
    "project_duration": 1000,
    "project_actual_duration": 2000,
    "activities": [
        {
            "name": "Ground Improvement PVD PA",
            "duration": 510,
            "cost": 67.116,
            "predecessors": [],
            "resource_requirements": [1, 178, 1]
        },
        {
            "name": "Ground Improvement PVD NPA",
            "duration": 798,
            "cost": 24.276,
            "predecessors": [],
            "resource_requirements": [1, 61, 1]
        },
        {
            "name": "Site Grading PA",
            "duration": 207,
            "cost": 48.552,
            "predecessors": [1],
            "resource_requirements": [1, 293, 1]
        },
        {
            "name": "Site Grading NPA",
            "duration": 52,
            "cost": 17.136,
            "predecessors": [2],
            "resource_requirements": [1, 411, 1]
        },
        {
            "name": "Buildings",
            "duration": 849,
            "cost": 13.328,
            "predecessors": [3],
            "resource_requirements": [3, 3, 3]
        },
        {
            "name": "Internal road PA",
            "duration": 284,
            "cost": 93.296,
            "predecessors": [3],
            "resource_requirements": [38, 57, 95]
        },
        {
            "name": "Internal road NPA",
            "duration": 235,
            "cost": 39.98,
            "predecessors": [4],
            "resource_requirements": [19, 29, 49]
        },
        {
            "name": "Grade Separator",
            "duration": 831,
            "cost": 33.320,
            "predecessors": [6],
            "resource_requirements": [5, 7, 11]
        },
        {
            "name": "Water Supply network",
            "duration": 823,
            "cost": 14.280,
            "predecessors": [3, 4],
            "resource_requirements": [7, 1, 11]
        },
        {
            "name": "Recycled water supply network",
            "duration": 800,
            "cost": 4.760,
            "predecessors": [3, 4],
            "resource_requirements": [2, 1, 4]
        },
        {
            "name": "Sewerage Network",
            "duration": 285,
            "cost": 28.560,
            "predecessors": [3, 4],
            "resource_requirements": [43, 1, 65]
        },
        {
            "name": "Power Supply",
            "duration": 285,
            "cost": 64.26,
            "predecessors": [3, 4],
            "resource_requirements": [98, 1, 147]
        },
        {
            "name": "Landscaping",
            "duration": 285,
            "cost": 3.332,
            "predecessors": [3, 4],
            "resource_requirements": [4, 1, 8]
        },
        {
            "name": "Project Commisioning",
            "duration": 39,
            "cost":  23.8,
            "predecessors": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            "resource_requirements": [397, 266, 1]
        }
    ]}


@app.route('/sez', methods=['POST'])
def createChartFromInputs():
    # incomes.append(request.get_json())

    activities = []

    # json_from_request = user_input_json_sample
    json_from_request = request.get_json()

    activities_json = json_from_request['activities']
    acivities_count = len(activities_json)
    for i in range(acivities_count):
        current_activity = activities_json[i]
        activities.append(Activity(
            current_activity['name'], current_activity['duration'], current_activity['cost'], current_activity['predecessors'], current_activity['resource_requirements']))

    # activities.append(Activity('Ground Improvement PVD-PA',
    #                            470, 67.116, [], [1, 178, 1]))
    # activities.append(Activity('Ground Improvement PVD-NPA',
    #                            494, 24.276, [], [1, 61, 1]))
    # activities.append(Activity('Site Grading PA',
    #                   207, 48.552, [1], [1, 293, 1]))
    # activities.append(Activity('Site Grading NPA',
    #                   52, 17.136, [2], [1, 411, 1]))
    # activities.append(Activity('Buildings', 849, 13.328, [3], [3, 3, 3]))
    # activities.append(Activity('Internal road PA',
    #                   284, 93.296, [3], [38, 57, 95]))
    # activities.append(Activity('Internal road NPA',
    #                   235, 39.98, [4], [19, 29, 49]))
    # activities.append(Activity('Grade Separator',
    #                   831, 33.320, [6], [5, 7, 11]))
    # activities.append(Activity('Water Supply network',
    #                            823, 14.280, [3, 4], [7, 1, 11]))
    # activities.append(Activity('Recycled water supply network',
    #                            800, 4.760, [3, 4], [2, 1, 4]))
    # activities.append(Activity('Sewerage Network', 285,
    #                            28.560, [3, 4], [43, 1, 65]))
    # activities.append(Activity('Power Supply', 285,
    #                   64.26, [3, 4], [98, 1, 147]))
    # activities.append(Activity('Landscaping', 285, 3.332, [3, 4], [4, 1, 8]))
    # activities.append(Activity('Project Commisioning', 39,
    #                            23.8, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], [397, 266, 1]))

    tempx = createChart(activities)

    img = Image.open("aa.png")
    rawBytes = io.BytesIO()
    img.save(rawBytes, 'PNG')
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    base64String = 'data:image/jpeg;base64,' + str(img_base64).split('\'')[1]

    response = flask.jsonify(
        {'response': base64String, 'message': tempx})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

    # return '', 204


if __name__ == "__main__":
    app.run()

# Define the project parameters
max_duration = 850
max_cost = 100
num_resources = 3
max_resource_capacity = 400

# Define the genetic algorithm parameters
population_size = 50
mutation_rate = 0.01
num_generations = 100


class UserInput:
    def __init__(self, project_name, project_duration, project_actual_duration, activities):
        self.project_name = project_name
        self.project_duration = project_duration
        self.project_actual_duration = project_actual_duration
        self.activities = activities


class Activity:
    def __init__(self, name, duration, cost, predecessors, resource_requirements):
        self.name = name
        self.duration = duration
        self.cost = cost
        self.predecessors = predecessors
        self.resource_requirements = resource_requirements


def generate_random_schedule(activities):
    num_activities = len(activities)
    schedule = np.zeros(num_activities)
    for i in range(num_activities):
        schedule[i] = random.randint(0, max_duration)
    return schedule


def calculate_total_cost(schedule, activities):
    total_cost = 0
    num_activities = len(activities)
    for i in range(num_activities):
        total_cost += schedule[i] * activities[i].cost
    return total_cost


def calculate_total_time(schedule, activities):
    num_activities = len(activities)
    total_time = np.zeros(num_activities)
    for i in range(num_activities):
        pred_time = [total_time[j] for j in activities[i].predecessors]
        if len(pred_time) > 0:
            total_time[i] = max(pred_time) + schedule[i]
        else:
            total_time[i] = schedule[i]

        # Adjust duration based on resource requirements
        resource_usage = sum(activities[i].resource_requirements)
        total_time[i] /= resource_usage

    return max(total_time)


def calculate_fitness(schedule, activities):
    total_cost = calculate_total_cost(schedule, activities)
    total_time = calculate_total_time(schedule, activities)
    return 1 / (total_cost * total_time)


def crossover(parent1, parent2, activities):
    num_activities = len(activities)
    crossover_point = random.randint(1, num_activities - 2)
    child = np.concatenate(
        (parent1[:crossover_point], parent2[crossover_point:]))
    return child


def mutate(schedule, activities):
    num_activities = len(activities)
    for i in range(num_activities):
        if random.random() < mutation_rate:
            # Increase the resources to decrease the duration
            # Adjust the factor range as desired
            resource_factor = random.uniform(0.7, 0.9)
            for j in range(num_resources):
                activities[i].duration /= activities[i].resource_requirements[j]
                activities[i].resource_requirements[j] *= resource_factor
                activities[i].duration *= activities[i].resource_requirements[j]
    return schedule


def genetic_algorithm(activities):
    population = []
    for _ in range(population_size):
        schedule = generate_random_schedule(activities)
        population.append(schedule)

    for generation in range(num_generations):
        fitness_scores = []
        for schedule in population:
            fitness_scores.append(calculate_fitness(schedule, activities))

        # Select parents based on fitness scores
        parents_indices = np.random.choice(
            len(population), size=2, replace=False, p=fitness_scores / np.sum(fitness_scores))
        parent1 = population[parents_indices[0]]
        parent2 = population[parents_indices[1]]

        # Perform crossover and mutation
        child = crossover(parent1, parent2, activities)
        child = mutate(child, activities)

        # Replace the least fit individual with the child
        least_fit_index = np.argmin(fitness_scores)
        population[least_fit_index] = child

        best_schedule = population[np.argmax(fitness_scores)]
        best_cost = calculate_total_cost(best_schedule, activities)
        best_time = calculate_total_time(best_schedule, activities)

        print(f"Generation: {generation + 1}  Best Time: {best_time}")

    return best_schedule


def plot_gantt_chart(activities, schedule):
    fig, ax = plt.subplots()

    # Set the y-axis ticks and labels
    y_ticks = range(len(activities))
    y_labels = [f"{activities[i].name}" for i in y_ticks]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)

    # Calculate the start and end times for each activity
    start_times = [0] * len(activities)
    end_times = [0] * len(activities)
    for i, activity in enumerate(activities):
        predecessors = activity.predecessors
        if len(predecessors) > 0:
            max_end_time = max([end_times[pred-1] for pred in predecessors])
            start_times[i] = max_end_time
        end_times[i] = start_times[i] + activity.duration

    # Plot the Gantt chart bars
    for i, activity in enumerate(activities):
        start_time = start_times[i]
        end_time = end_times[i]
        duration = activity.duration

        rounded_duration = round(duration)

        # Plot the bar for the activity
        ax.barh(i, rounded_duration, left=start_time,
                height=0.5, align='center')

        # Add the duration text to the right side of the bar
        ax.text(end_time, i,
                f"{rounded_duration} days", ha='left', va='center')

    # Set the x-axis limits and labels
    max_time = max(end_times)
    ax.set_xlim(0, round(max_time, 2))
    ax.set_xlabel('Time (days)')

    # Set the title
    ax.set_title('Project Schedule Gantt Chart')

    # Display the Gantt chart
    # plt.show()
    plt.savefig("aa.png")


# Rest of the code...


def calculate_start_and_end_times(activities, optimized_schedule):
    smallest_start_time = float('inf')
    maximum_end_time = 0

    start_times = [0] * len(activities)
    end_times = [0] * len(activities)
    for i, activity in enumerate(activities):
        predecessors = activity.predecessors
        if len(predecessors) > 0:
            max_end_time = max([end_times[pred-1] for pred in predecessors])
            start_times[i] = max_end_time
        end_times[i] = start_times[i] + activity.duration
        if start_times[i] < smallest_start_time:
            smallest_start_time = start_times[i]
        if end_times[i] > maximum_end_time:
            maximum_end_time = end_times[i]

    # for i, activity in enumerate(activities):
    #     print(activities[i].name)
    #     start_time = sum(optimized_schedule[:i])  # Calculate the start time of the activity
    #     end_time = start_time + activities[i].duration  # Calculate the end time of the activity

    #     if start_time < smallest_start_time:
    #         smallest_start_time = start_time
    #     if end_time > maximum_end_time:
    #         maximum_end_time = end_time

    return smallest_start_time, maximum_end_time


def createChart(activities):

    best_schedule = genetic_algorithm(activities)
    print("Optimized Schedule:")

    num_activities = len(activities)
    for i in range(num_activities):
        print(
            f"Activity_name:{activities[i].name}, Duration: {activities[i].duration}")

    # Calculate the smallest start time and maximum end time
    smallest_start_time, maximum_end_time = calculate_start_and_end_times(
        activities, best_schedule)

    print("Smallest Start Time:", smallest_start_time)
    print("Maximum End Time:", maximum_end_time)

    # Generate a random schedule (replace this with your own schedule)
    # schedule = generate_random_schedule(activities)

    # Plot the Gantt chart
    plot_gantt_chart(activities, best_schedule)
    return round(maximum_end_time, 0)