* Basic Reset and Variables */
:root {
    --bg-dark: #1e1e1e; /* Main dark background */
    --text-light: #e0e0e0; /* Main light text color */
    --text-faded: #a0a0a0; /* Faded/secondary text color */
    --input-bg: #333333; /* Input box background */
    --accent-color: #ff9966; /* Orange/Copper accent for the asterisk */
    --border-color: #444444; /* Border/separator color */
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* Body and Main Container Styling (Dark Theme) */
body {
    background-color: var(--bg-dark);
    color: var(--text-light);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 900px; /* Constrain the width of the main content */
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Top Bar Styling (Free Plan/Upgrade) */
.top-bar {
    position: absolute;
    top: 50px; 
    display: flex;
    gap: 10px;
    padding: 5px 15px;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    font-size: 0.9em;
    color: var(--text-faded);
}

.upgrade-btn {
    background-color: var(--input-bg);
    color: var(--text-light);
    border: none;
    padding: 3px 10px;
    border-radius: 15px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.upgrade-btn:hover {
    background-color: #444444;
}

/* Greeting Header Styling */
.greeting {
    margin-top: 150px; 
    margin-bottom: 20px;
    font-size: 2.5em;
    font-weight: 300;
    text-align: center;
}

.asterisk {
    color: var(--accent-color);
    margin: 0 5px;
    font-size: 1.2em;
}

/* Interaction Area */
.interaction-area {
    width: 100%;
    max-width: 700px; 
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* The prompt-text is now visually removed/redundant as the input box has a placeholder */
.prompt-text {
    /* Keeping the class, but giving it a functional role if needed, or simply removing it in the final HTML */
    display: none; 
}


/* Input Box Wrapper (The main change for the bottom controls layout) */
.input-box-wrapper {
    width: 100%;
    background-color: var(--input-bg);
    border-radius: 15px;
    padding: 15px;
    
    /* Use flex to stack elements (textarea and bottom-controls) */
    display: flex; 
    flex-direction: column; 
    gap: 10px; /* Space between the text area and the controls row */
    
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

/* Text Area Styling */
.input-box {
    width: 100%;
    min-height: 80px;
    background: none;
    border: none;
    color: var(--text-light);
    font-size: 1em;
    resize: none;
    padding: 0 10px;
    outline: none;
}

/* Standard placeholder selector for cross-browser compatibility */
.input-box::placeholder {
    color: var(--text-faded);
    font-style: italic;
    opacity: 1; /* For Firefox */
}

/* New: Container for the controls at the very bottom */
.bottom-controls {
    width: 100%;
    /* Use flexbox to space the left controls and right model-select */
    display: flex;
    justify-content: space-between; 
    align-items: center;
    padding-top: 5px; 
    border-top: 1px solid var(--border-color); 
}

/* Group for the left-side buttons */
.controls {
    /* Use the same class name from the HTML, but apply the style for the left group */
    display: flex;
    gap: 5px;
    align-items: center;
}

.control-btn {
    background: none;
    border: 1px solid var(--border-color);
    color: var(--text-faded);
    padding: 5px 10px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.2em;
    line-height: 1;
    transition: background-color 0.2s;
}

.control-btn:hover {
    background-color: #444444;
}

/* Group for the right-side model selector */
.model-select {
    /* Use the same class name from the HTML, but apply the style for the right group */
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--text-faded);
    font-size: 0.9em;
}

.model-btn {
    background-color: var(--accent-color);
    color: var(--bg-dark);
    border: none;
    padding: 5px 10px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
}

/* Suggestion Pills Styling */
.suggestion-pills {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 10px;
}

.pill {
    background-color: var(--bg-dark);
    color: var(--text-faded);
    border: 1px solid var(--border-color);
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9em;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: background-color 0.2s, border-color 0.2s;
}

.pill:hover {
    background-color: #2b2b2b;
    border-color: var(--text-faded);
}

.pill-icon {
    font-size: 1.1em;
}
