# Solar Data Visualizer 
SolarDataVisualizer is a React-based web application designed to visualize solar data. This project uses React along with Leaflet for map rendering and TailwindCSS for styling.

## Getting Started
These instructions will guide you through setting up and running SolarDataVisualizer on your local machine for development and testing purposes.

### Prerequisites
Before you begin, ensure you have the following installed:

- Git: To Clone the repository
- Node.js: To run the application locally

### Installation

1- clone the repository:
```bash
git clone https://github.com/ibrhmch/SolarDataVisualizer.git
```
Now Navigate to the project directory:
```bash
cd SolarDataVisualizer
```

2- Install Node:
If you don't have node installed, you can download it from [here](https://nodejs.org/en).

To Confirm node installed succesfully, run this command:
```bash
node -v
```

3- Install dependencies by running this in project directory:
```bash
npm install
```

4- Run the application:
```bash
npm start
```

The application should now be running on [localhost:3000](http://localhost:3000).

5- View the Application:
Open your browser and navigate to [localhost:3000](http://localhost:3000).


# To use the Dockerfile and spin up a container
1- Build the image
`docker build -t reactapp .`

2- Create a container and forward the port using:
`docker run -p 8080:80 reactapp`


*Started: 12/1/2023*
