import json
from flask import Flask, render_template, redirect, url_for, request, flash
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For flash messages

# Load incidents from the JSON file
def load_incidents():
    try:
        with open('incidents.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save incidents to the JSON file
def save_incidents(incidents):
    with open('incidents.json', 'w') as f:
        json.dump(incidents, f, indent=4)

@app.route('/')
def home():
    incidents = load_incidents()
    return render_template('home.html', incidents=incidents)

@app.route('/add', methods=['GET', 'POST'])
def add_incident():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        # Generate a unique incident ID
        incident_id = str(uuid.uuid4())
        
        incidents = load_incidents()
        incidents[incident_id] = {
            'title': title,
            'description': description
        }
        
        save_incidents(incidents)
        flash('Incident added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_incident.html')

@app.route('/edit/<incident_id>', methods=['GET', 'POST'])
def edit_incident(incident_id):
    incidents = load_incidents()
    incident = incidents.get(incident_id)
    
    if not incident:
        flash('Incident not found!', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        incident['title'] = request.form['title']
        incident['description'] = request.form['description']
        save_incidents(incidents)
        flash('Incident updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_incident.html', incident=incident, incident_id=incident_id)

@app.route('/delete/<incident_id>', methods=['POST'])
def delete_incident(incident_id):
    incidents = load_incidents()
    
    if incident_id in incidents:
        del incidents[incident_id]
        save_incidents(incidents)
        flash('Incident deleted successfully!', 'success')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
