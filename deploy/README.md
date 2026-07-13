# Deploy — systemd

## Atualização automática de preços (timer)

Roda `python manage.py atualizar_precos` a cada 6h (00, 06, 12, 18h).
Como o token do ML agora vive no banco (model `MLToken`), a renovação feita
pelo timer é compartilhada com os workers do gunicorn — não precisa mais de
`sudo systemctl restart whey-api` depois de renovar.

### Instalar (uma vez, no EC2)

```bash
cd /home/ubuntu/projeto-whey
sudo cp deploy/whey-precos.service /etc/systemd/system/
sudo cp deploy/whey-precos.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now whey-precos.timer
```

### Verificar / operar

```bash
systemctl list-timers whey-precos.timer      # proximo disparo
sudo systemctl start whey-precos.service     # rodar agora (manual)
journalctl -u whey-precos.service -n 50      # ver saida da ultima rodada
```
