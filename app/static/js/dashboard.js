/* ========== GLOBAL ========== */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background: #f4f6f9;
    color: #333;
}

/* ========== SIDEBAR ========== */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 10%;
    height: 100vh;
    background: #004080;
    color: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 2rem;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
}

.sidebar h2 {
    color: #fff;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.sidebar button,
.sidebar .logout-btn {
    width: 80%;
    background: #0066cc;
    color: #fff;
    border: none;
    margin-bottom: 1rem;
    padding: 0.7rem;
    border-radius: 5px;
    font-size: 0.9rem;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
}

.sidebar button:hover,
.sidebar .logout-btn:hover {
    background: #0052a3;
}

/* ========== MAIN CONTENT ========== */
.content {
    margin-left: 10%;
    padding: 2rem;
}

/* ========== CHART ========== */
.chart-container {
    background: #fff;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    max-width: 900px;
    margin: auto;
}

canvas {
    width: 100% !important;
    height: auto !important;
}

/* ========== TABLES ========== */
.table-test {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

.table-test th, .table-test td {
    padding: 0.8rem;
    text-align: center;
    border-bottom: 1px solid #ddd;
}

.table-test th {
    background: #f0f4f9;
    color: #004080;
    font-weight: bold;
}

/* ========== FORMS ========== */
form {
    max-width: 900px;
    margin: auto;
    background: #fff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

fieldset {
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 2rem;
    padding: 1.5rem;
}

legend {
    font-weight: bold;
    font-size: 1.1rem;
    color: #004080;
}

label {
    display: block;
    margin-bottom: 1rem;
}

input[type="text"],
input[type="number"],
select {
    width: 100%;
    padding: 0.6rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 0.3rem;
}

.field-group {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.btn-save, .btn-send {
    background: #004080;
    color: #fff;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
}

.btn-save:hover, .btn-send:hover {
    background: #003366;
}

/* ========== RESPONSIVE DESIGN ========== */
@media (max-width: 1024px) {
    .sidebar {
        width: 15%;
    }
    .content {
        margin-left: 15%;
    }
}

@media (max-width: 768px) {
    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
        flex-direction: row;
        justify-content: space-around;
        box-shadow: none;
    }
    .content {
        margin-left: 0;
        padding: 1rem;
    }
    .chart-container, form {
        max-width: 100%;
    }
    .table-test {
        font-size: 0.85rem;
        overflow-x: auto;
        display: block;
        white-space: nowrap;
    }
}

@media (max-width: 480px) {
    body {
        font-size: 0.9rem;
    }
    .sidebar button {
        font-size: 0.8rem;
        padding: 0.5rem;
    }
    input[type="text"],
    input[type="number"],
    select {
        font-size: 0.9rem;
    }
}
