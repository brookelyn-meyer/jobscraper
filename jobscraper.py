import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tkinter as tk
from tkinter import messagebox

def open_link(event):
    widget = event.widget
    index = widget.index(tk.CURRENT)
    link = widget.get(f"{index} linestart", f"{index} lineend")
    webbrowser.open(link)

def find_jobs():
    # Get the URL and keyword filters entered by the user
    url = entry_url.get()
    keywords = {
        "years_exp": entry_years_exp.get(),
        "entry_level": entry_entry_level.get().split(',')
    }

    # Scrape jobs from the entered URL with keyword filters
    find_jobs_from_site(url, keywords)

def find_jobs_from_site(url, keywords):
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        job_links = []
        domain = urlparse(url).netloc

        # Scraping logic based on the structure of the website (modify this accordingly)
        if domain == 'www.linkedin.com':
            job_listings = soup.find_all('a', class_='base-card__full-link')
            job_links = [job['href'] for job in job_listings if any(all(keyword.lower() in job.text.lower() for keyword in keyword_list.split()) for keyword_list in keywords['entry_level'])]
        elif domain == 'www.indeed.com':
            job_listings = soup.find_all('div', class_='jobsearch-SerpJobCard')
            job_links = [job.find('a', class_='jobtitle')['href'] for job in job_listings if any(all(keyword.lower() in job.text.lower() for keyword in keyword_list.split()) for keyword_list in keywords['entry_level'])]
        elif domain == 'jobs.google.com':  # Example for handling Google Jobs (You may need to adjust this based on Google Jobs HTML structure)
            job_listings = soup.find_all('div', class_='example-class')  # Replace 'example-class' with the actual class used in Google Jobs
            job_links = [job.find('a')['href'] for job in job_listings if any(all(keyword.lower() in job.text.lower() for keyword in keyword_list.split()) for keyword_list in keywords['entry_level'])]

        # Display job links in the GUI
        if job_links:
            for link in job_links:
                parsed_link = urlparse(link)
                link_text = f"{parsed_link.netloc}{parsed_link.path}\n"
                text_widget.insert(tk.END, link_text)
                text_widget.tag_add("link", text_widget.index("end-1l"), text_widget.index("end-1c"))
        else:
            messagebox.showinfo("Info", f"No job links found for {domain} based on specified filters.")

def clear_links():
    text_widget.delete("1.0", tk.END)

# GUI setup
root = tk.Tk()
root.title("Job Scraper")
root.geometry("600x500")  # Setting window size

# Styling
root.configure(bg="#f0f0f0")

header_label = tk.Label(root, text="Find Jobs", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
header_label.pack(fill="x", padx=10, pady=10)

# URL Entry Field
url_frame = tk.Frame(root, bg="#f0f0f0")
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="Enter job website URL:", font=("Arial", 12), bg="#f0f0f0")
url_label.pack(side=tk.LEFT, padx=5)

entry_url = tk.Entry(url_frame, width=50, font=("Arial", 10))
entry_url.pack(side=tk.LEFT, padx=5)

# Keyword Filters
filters_frame = tk.Frame(root, bg="#f0f0f0")
filters_frame.pack(pady=10)

label_years_exp = tk.Label(filters_frame, text="Years of Experience:", font=("Arial", 12), bg="#f0f0f0")
label_years_exp.pack(side=tk.LEFT, padx=5)

entry_years_exp = tk.Entry(filters_frame, width=10, font=("Arial", 10))
entry_years_exp.pack(side=tk.LEFT, padx=5)

label_entry_level = tk.Label(filters_frame, text="Keywords (Separated by commas):", font=("Arial", 12), bg="#f0f0f0")
label_entry_level.pack(side=tk.LEFT, padx=5)

entry_entry_level = tk.Entry(filters_frame, width=40, font=("Arial", 10))
entry_entry_level.pack(side=tk.LEFT, padx=5)

# Find Jobs Button
button = tk.Button(root, text="Search jobs", command=find_jobs, font=("Arial", 12), bg="#4CAF50", fg="white")
button.pack(pady=10)

# Clear Links Button
clear_button = tk.Button(root, text="Clear Links", command=clear_links, font=("Arial", 12))
clear_button.pack()

# Job Links Text Widget
text_widget = tk.Text(root, width=80, height=20, font=("Arial", 10))
text_widget.pack(padx=10, pady=5)

# Configure tags for clickable links
text_widget.tag_configure("link", foreground="blue", underline=True)

# Bind link tags to open in browser on click
text_widget.tag_bind("link", "<Button-1>", open_link)

root.mainloop()
