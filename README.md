# Road Trips & Hikes API service

### Note: This project is still under development.

## Purpose

In order to protect credentials & API keys when using data from public APIs like Flickr and Blogger, this service makes an authenticated call to the provider API and forwards only the necessary fields via a JSON to a "wrapper" call.

By storing all the sensitive information in a separate JSON file *outside of source control*, all the Django code can be commited to GitHub including the Settings.py and views.py which are passing the API keys.

## Future Plans

This repo is basically a clone of https://github.com/lar-mo/pmd_api

Thanks to how Django works, I may add other Django apps like an RESTapi, a custom CMS, and new template-based frontend for RTAH.
