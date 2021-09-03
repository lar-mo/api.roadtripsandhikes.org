# Road Trips & Hikes API service

### Note: This project is still under development.

## Purpose

In order to protect credentials & API keys when using data from public APIs like Flickr and Blogger, this service makes an authenticated call to the original endpoint and only forwards the necessary fields (JSON) in a "wrapper" call used by the frontend.

Additionally, because all the sensitive information is kept in a separate JSON file *outside of source control*, the Django code can be safely commited to GitHub.

## Future Plans

This repo is basically a clone of https://github.com/lar-mo/pmd_api

Thanks to how Django works, I may add other Django apps like an RESTapi, a custom CMS, and new template-based frontend for RTAH.
