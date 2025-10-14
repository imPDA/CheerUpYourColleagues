## Cheer Up Your Colleagues

This is an educational programming project for the Quantori DE School. The objective was to create an application that retrieves an image and a quote, combines them, and sends the result to a Microsoft Teams chat. The entire application is orchestrated by Apache Airflow. Images and quotes are stored in an S3-compatible storage system (e.g., MinIO) and an RDS (AWS) database, respectively, after being sent to the chat.

The entire application is containerized using Docker. Git is used for version control, with a new feature branch (following the naming convention MSI-...) created for each development sprint. Development is conducted on the dev branch.
