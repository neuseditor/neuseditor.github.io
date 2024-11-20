import os

# Directory paths
output_dir = "survey_experiments"

# Template for the static HTML files
template = """<!DOCTYPE html>
<html>
<head>
    <title>Video Survey Experiment {experiment_number}</title>
    <link rel="stylesheet" type="text/css" href="survey_static/css/styles.css">
    <style>
        .video-container-row {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .video-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .ranking {{
            margin-top: 10px;
        }}
        .hidden-option {{
            display: none;
        }}
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const selects = document.querySelectorAll("select");
            const submitButton = document.querySelector("button[type='submit']");
            const resetButton = document.createElement("button");

            function updateSelectOptions() {{
                const values = Array.from(selects).map(s => s.value).filter(v => v !== "");
                selects.forEach(s => {{
                    Array.from(s.options).forEach(option => {{
                        if (values.includes(option.value) && option.value !== s.value) {{
                            option.classList.add("hidden-option");
                        }} else {{
                            option.classList.remove("hidden-option");
                        }}
                    }});
                }});
                // Enable the submit button only if all scores are selected
                submitButton.disabled = values.length !== selects.length;
            }}

            selects.forEach(select => {{
                select.addEventListener("change", function() {{
                    updateSelectOptions();
                }});
            }});

            // Add reset button functionality
            resetButton.type = "button";
            resetButton.textContent = "Reset Scores";
            resetButton.style.marginRight = "10px";
            resetButton.addEventListener("click", function() {{
                selects.forEach(select => {{
                    select.value = "";
                }});
                updateSelectOptions();
            }});
            document.querySelector("form").insertBefore(resetButton, document.querySelector("div[style='text-align: right;']"));

            // Initial call to hide options based on preselected values
            updateSelectOptions();
        }});
    </script>
</head>
    <div style="background-color: #f9f9f9; padding: 20px; border-bottom: 1px solid #ccc;">
        <p style="text-align: center; font-weight: bold;">
            Note: This is a dummy survey, created as a replica of the actual survey. Unlike the actual survey, your scores here are not logged and the video order is not randomized. 
            <br>The video order is: IN2N, PDS-NeRF, PDS-Splat, and ours. To proceed to the next survey, you must fill in all scores, just as in the actual survey. 
            <br>To go back to the survey page, click <a href="survey_index.html">here</a>. To go back to the main page, click <a href="../index.html">here</a>.
        </p>
    </div>
    <h1>Score the Videos from Best (3) to Worst (0)</h1>
    <h1 style="text-align: center;">Input data:</h1>
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="survey_static/images/experiment_{experiment_number}.jpg" alt="Explanation Image" width="1340">
    </div>
    <h3 style="text-align: center;">
        <em>Considering the original scene images and editing text prompts,<br>
        give an overall score to the following scenes in terms of geometry,<br>
        editing quality, and clarity while preserving the features of the original scene.</em>
    </h3>
    <h1 style="text-align: center;">Output:</h1>
    <form method="get" action="{next_experiment}">
        <div class="video-container-row">
            {video_containers}
        </div>
        <h4 style="text-align: center;">
            <em>Please score all the options</em>
        </h4>
        <div style="text-align: right;">
            <button type="submit" disabled>Submit Scores</button>
        </div>
    </form>
    <br><br>
</body>
</html>
"""

# Video container template
video_container_template = """
<div class="video-container">
    <video width="320" controls loop autoplay muted>
        <source src="survey_static/videos/experiment_{experiment_number}_video_{video_number}.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div class="ranking">
        <label for="ranking_{video_number}">Score:</label>
        <select name="ranking_{video_number}" id="ranking_{video_number}">
            <option value="" disabled selected>Choose score</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
        </select>
    </div>
</div>
"""

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Generate HTML files for each experiment
for experiment_number in range(1, 35):
    # Create video containers for the experiment
    video_containers = "".join(
        [video_container_template.format(experiment_number=experiment_number, video_number=video_number%4 + 1)
         for video_number in range(1, 5)]
    )
    
    # Fill in the template
    next_experiment = f"experiment_{experiment_number + 1}.html" if experiment_number < 34 else "survey_thank_you.html"
    html_content = template.format(experiment_number=experiment_number, video_containers=video_containers, next_experiment=next_experiment)
    
    # Write the HTML file
    output_file_path = os.path.join(output_dir, f"experiment_{experiment_number}.html")
    with open(output_file_path, "w") as f:
        f.write(html_content)

# Generate survey_index.html
index_template = """<!DOCTYPE html>
<html>
<head>
    <title>Experiment Survey Index</title>
    <link rel="stylesheet" type="text/css" href="survey_static/css/styles.css">
</head>
    <div style="background-color: #f9f9f9; padding: 20px; border-bottom: 1px solid #ccc;">
        <p style="text-align: center; font-weight: bold;">
            Note: This is a dummy survey, created as a replica of the actual survey. Unlike the actual survey, your scores here are not logged and the video order is not randomized. 
            <br> The video order is: IN2N, PDS-NeRF, PDS-Splat, and ours. To proceed to the next survey, you must fill in all scores, just as in the actual survey.
            <br> To go back to the main page, click <a href="../index.html">here</a>.
        </p>
    </div>
    <h1>Select an Experiment</h1>
    <ul class="experiment-list">
        {experiment_links}
    </ul>
</body>
</html>
"""

# Create links for all experiments
experiment_links = "".join(
    [f"<li><a href=\"experiment_{experiment_number}.html\">Experiment {experiment_number}</a></li>" for experiment_number in range(1, 35)]
)

# Fill in the index template
index_content = index_template.format(experiment_links=experiment_links)

# Write the survey_index.html file
index_file_path = os.path.join(output_dir, "survey_index.html")
with open(index_file_path, "w") as f:
    f.write(index_content)

print(f"Generated HTML files for 34 experiments and survey_index.html in '{output_dir}' directory.")
