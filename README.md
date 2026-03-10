
# 🇵🇹 Edenred Portugal — Home Assistant Integration

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![License](https://img.shields.io/github/license/FragMenthor/home-assistant-custom-components-edenred_pt)
![Release](https://img.shields.io/github/v/release/FragMenthor/home-assistant-custom-components-edenred_pt)

Integração para obter saldos e movimentos dos cartões **Edenred Portugal** diretamente no Home Assistant.

## ✨ Funcionalidades

- Login com autenticação oficial da Edenred
- Token armazenado em memória (nunca no disco)
- Suporte para **vários cartões**
- Atualização configurável: **15 min a 12 horas**
- Sensor de saldo por cartão
- Sensor de último movimento (com atributos completos)
- Compatível com **HACS (Custom Repo)**

## 📦 Instalação via HACS

1. Em **HACS → Custom repositories**, adicionar `https://github.com/FragMenthor/home-assistant-custom-components-edenred_pt`
2. Tipo: **Integration**
3. Instalar e reiniciar o Home Assistant

## 🔧 Configuração

1. **Configurações → Dispositivos e Serviços → Adicionar Integração**
2. Procurar **Edenred Portugal**
3. Introduzir Email, Password e Intervalo de atualização (15–720 min)

## 🧩 Sensores criados

Para cada cartão são criados dois sensores:

- `sensor.edenred_<id>_saldo`
- `sensor.edenred_<id>_ultimo_movimento`

Atributos do último movimento:
- `date`, `description`, `category`, `balance_after`

## 📜 Licença

MIT License
