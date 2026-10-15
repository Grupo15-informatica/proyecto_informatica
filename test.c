#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    char peticion[100];
    char respuesta[100];

    // Inicializamos respuesta vacía
    respuesta[0] = '\0';

    // Cadena de entrada exacta del vídeo
    strcpy(peticion, "Miguel/47/Juan/12/Maria/22/Marcos/19");

    char nombre[20];
    int edad;
    
    // Extraemos el primer nombre con el separador "/"
    char *p = strtok(peticion, "/");

    while (p != NULL)
    {
        strcpy(nombre, p);             // Copiamos el nombre
        p = strtok(NULL, "/");          // Extraemos la edad
        edad = atoi(p);                // Convertimos la edad a entero
        
        if (edad > 18) {
            // Concatenamos en respuesta: "nombre*edad-"
            sprintf(respuesta, "%s%s*%d-", respuesta, nombre, edad);
        }
        
        p = strtok(NULL, "/");          // Extraemos el SIGUIENTE nombre
    }

    // Eliminamos el último guión '-' sobrante
    if (strlen(respuesta) > 0) {
        respuesta[strlen(respuesta) - 1] = '\0';
    }

    // Mostramos el resultado por la consola de Zinjai
    printf("Resultado: %s\n", respuesta);

    return 0;
}
