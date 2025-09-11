# FF-BASE AI Search Frontend

Frontend application for the FF-BASE AI Search system.

## Technologies Used

- Vanilla JavaScript
- Tailwind CSS (via local build)
- Font Awesome (for icons)
- Firebase Hosting

## Project Structure

```
.
├── index.html       # Main HTML file
├── script.js        # Main JavaScript file
├── server.js        # Express server for Firebase functions
├── package.json     # Project dependencies and scripts
└── ...
```

## Available Scripts

- `npm start` - Start the Node.js server
- `npm run start-python` - Start a Python HTTP server on port 3000
- `npm run deploy` - Deploy to Firebase Hosting
- `npm run build:css` - Build Tailwind CSS
- `npm run build` - Build all assets

## Development

To run the frontend locally:

1. Start the backend server (see backend README)
2. Run `npm start` to start the frontend server
3. Open `http://localhost:3000` in your browser

For easier development, you can use the `start-dev.sh` script in the scripts directory to start both backend and frontend simultaneously.

If you make changes to the styles, you can rebuild the CSS using:
```bash
./rebuild-css.sh
```

### Running the Frontend Server

To start the frontend development server:
```bash
npm start
```

This will start the Node.js server on port 3000. The frontend will be available at http://localhost:3000

Alternatively, you can use the Python HTTP server:
```bash
npm run start-python
```

However, the Node.js server is recommended as it provides better functionality for the application.

## Editing the Interface

Detailed instructions on how to edit interface elements can be found in:
- `EDITING_GUIDE.md` - Comprehensive guide to editing the interface
- `EDITING_EXAMPLES.md` - Practical examples of interface modifications

Key files for editing:
- `index.html` - Main HTML structure
- `styles/globals.css` - Custom CSS styles and variables
- `script.js` - JavaScript functionality

## shadcn/ui Integration

This project has been configured to use shadcn/ui components with a vanilla JavaScript setup. 
See `SHADCN_UI.md` for more information on how to use and extend the components.

## Deployment

To deploy to Firebase Hosting:

1. Run `npm run deploy`
2. The site will be available at the configured Firebase URL