# Scraping tarea

Para poder usar este repositorio se necesitan descargar las siguientes librerias 

```
pip install requests beautifulsoup4
```

Luego dentro del proyecto, se hace una peticion get a una wikipedia de pokemon

si responde un estatus 200 lo parsea en formato html 

luego se hace un rejunte de las etiquetas 
```
<a>
```

y de eso se extraen todas las etiquetas 
```
<h1> y <p>
```
el resultado luego se te guarda en un Json llamado "output.json" en el cual se puede ver los resultados obtenidos
