#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <pthread.h>

int contador;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

int i;
int sockets[100];

void *AtenderCliente(void *socket)
{
	int sock_conn;
	int *s = (int *) socket;
	sock_conn = *s;

	char peticion[512];
	char respuesta[512];
	int ret;
	int terminar = 0;

	while (terminar == 0)
	{
		ret = read(sock_conn, peticion, sizeof(peticion));
		if (ret <= 0) break;

		peticion[ret] = '\0';
		printf("Peticion recibida: %s\n", peticion);

		char *p = strtok(peticion, "/");
		int codigo = atoi(p);
		int numForm = 0;
		float valor = 0.0;

		if (codigo != 0)
		{
			p = strtok(NULL, "/");
			if (p != NULL) numForm = atoi(p);

			p = strtok(NULL, "/");
			if (p != NULL) valor = atof(p);
		}

		if (codigo == 0)
		{
			terminar = 1;
		}
		else if (codigo == 1)
		{
			float fahrenheit = (valor * 9.0 / 5.0) + 32.0;
			sprintf(respuesta, "1/%d/%.2f", numForm, fahrenheit);
		}
		else if (codigo == 2)
		{
			float celsius = (valor - 32.0) * 5.0 / 9.0;
			sprintf(respuesta, "2/%d/%.2f", numForm, celsius);
		}

		if (codigo != 0)
		{
			printf("Respuesta: %s\n", respuesta);
			write(sock_conn, respuesta, strlen(respuesta));
		}

		if (codigo == 1 || codigo == 2)
		{
			pthread_mutex_lock(&mutex);
			contador = contador + 1;
			pthread_mutex_unlock(&mutex);

			char notificacion[20];
			sprintf(notificacion, "4/%d", contador);
			for (int j = 0; j < i; j++)
				write(sockets[j], notificacion, strlen(notificacion));
		}
	}

	close(sock_conn);
	return NULL;
}

int main(int argc, char *argv[])
{
	int sock_conn, sock_listen;
	struct sockaddr_in serv_adr;

	if ((sock_listen = socket(AF_INET, SOCK_STREAM, 0)) < 0)
		printf("Error creando socket\n");

	memset(&serv_adr, 0, sizeof(serv_adr));
	serv_adr.sin_family = AF_INET;
	serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_adr.sin_port = htons(9050);

	if (bind(sock_listen, (struct sockaddr *) &serv_adr, sizeof(serv_adr)) < 0)
		printf("Error al bind\n");

	if (listen(sock_listen, 3) < 0)
		printf("Error en el Listen\n");

	contador = 0;
	pthread_t thread;
	i = 0;

	for (;;)
	{
		printf("Escuchando peticiones...\n");
		sock_conn = accept(sock_listen, NULL, NULL);
		printf("Conexion aceptada\n");

		sockets[i] = sock_conn;
		pthread_create(&thread, NULL, AtenderCliente, &sockets[i]);
		i++;
	}
}
