<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat con IA</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #28a745;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        #respuesta {
            margin-top: 20px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #ccc;
            min-height: 50px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Pregúntale a la IA</h2>
        <input type="text" id="pregunta" placeholder="Escribe tu pregunta">
        <button onclick="enviarPregunta()">Enviar</button>
        <div id="respuesta">Esperando respuesta...</div>
    </div>

    <script>
        function enviarPregunta() {
            const pregunta = document.getElementById("pregunta").value;
            fetch(`/ia/${encodeURIComponent(pregunta)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("respuesta").innerText = data.Respuesta;
                })
                .catch(error => {
                    document.getElementById("respuesta").innerText = "Error al obtener la respuesta.";
                    console.error('Error:', error);
                });
        }
    </script>
</body>
</html>
