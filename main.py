from otto_api42 import intra
from html import escape as html_escape
import sys

pyear = 2025
pmonth = "august"
if len(sys.argv) == 3:
    pyear = int(sys.argv[1])
    pmonth = sys.argv[2]

client = intra.IntraAPIClient("config.yml")
users = client.pages_threaded(
    "campus/1/users", params={"filter[pool_year]": pyear, "filter[pool_month]": pmonth}
)
html = (
    """<!DOCTYPE html>
<html>
    <head>
        <title>"""
    + f"Pool viewer - {pmonth} {pyear}"
    + """</title>
        <style>
          body,
          html {
            margin: 0;
            padding: 0;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
          }

          body {
            width: 100vw;
          }

          figure {
            margin: 0;
          }

          figure img {
            width: 100%;
          }

          a {
            text-decoration: none;
            color: black;
          }

          .grid {
            display: flex;
            width: 100%;
            flex-wrap: wrap;
            justify-content: space-evenly;
            align-items: stretch;
            align-content: space-around;
          }

          .card {
            border: 1px solid #f0f0f0;
            border-radius: 8px;
            width: 15%;
            background-color: white;
            box-shadow: 0px 5px 10px -5px rgba(0, 0, 0, 0.4);
            padding: 8px;
          }
        </style>
    </head>
	<body>
		<div class="grid">"""
)
for user in users:
    html += f"""
			<div class="card">
				<a href="https://profile.intra.42.fr/users/{user.login}" target="_blank">
					<div class="card-content">
						<figure class="card-thumbnail">
							<img src={user.image.link} alt="Profile picture for {user.login}"/>
						</figure>
						<h3 class="card-title">{html_escape(user.usual_full_name)}</h3>
						<h4 class="card-subtitle">{user.login}</h4>
					</div>
				</a>
			</div>"""

html += """
		</div>
	</body>
</html>"""


with open("index.html", "w") as f:
    f.write(html)
