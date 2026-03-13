<p align="left">
  <img src="https://raw.githubusercontent.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/main/custom_components/edenred_pt/logo.png" alt="Edenred Portugal" width="500">
</p>

<p align="left">

  <!-- HACS (Custom Repo) -->
  <a href="https://hacs.xyz/">
    <img src="https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&logo=homeassistant&logoColor=white">
  </a>

  <!-- License -->
  <a href="https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt?style=for-the-badge">
  </a>

  <!-- Release -->
  <a href="https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/releases">
    <img src="https://img.shields.io/github/v/release/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt?style=for-the-badge&color=blue">
  </a>

  <!-- Downloads -->
  <a href="https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/releases">
    <img src="https://img.shields.io/github/downloads/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/total?style=for-the-badge&color=green">
  </a>

  <!-- Python version -->
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white">
  </a>

  <!-- Works with Home Assistant -->
  <a href="https://www.home-assistant.io/">
    <img src="https://img.shields.io/badge/Works%20with-Home%20Assistant%202025.12+-41BDF5?style=for-the-badge&logo=homeassistant&logoColor=white">
  </a>

  <!-- API Reverse Engineered -->
  <a href="#">
    <img src="https://img.shields.io/badge/API-Reverse%E2%80%91Engineered-red.svg?style=for-the-badge&logo=hackerone&logoColor=white">
  </a>

  <!-- Stars -->
  <a href="https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/stargazers">
    <img src="https://img.shields.io/github/stars/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt?style=for-the-badge&logo=github">
  </a>

  <!-- Issues -->
  <a href="https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/issues">
    <img src="https://img.shields.io/github/issues/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt?style=for-the-badge&color=yellow">
  </a>

</p>


# Edenred PT — Integração para Home Assistant

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange)
![License](https://img.shields.io/github/license/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt)
![Release](https://img.shields.io/github/v/release/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt)
![Language](https://img.shields.io/badge/language-PT-white)

Integração para obter saldos e movimentos dos cartões **Edenred Portugal** diretamente no Home Assistant.

## ✨ Funcionalidades

- Login com autenticação por **API NÃO OFICIAL** da Edenred
- Token temporário armazenado em memória
- Suporte para **vários cartões**
- Atualização configurável (e reconfigurável): **15 min a 12 horas**
- Sensor de saldo por cartão, com dados do cartão em atributos
- Sensor de último movimento (com atributos completos e histórico de movimentos)
- Compatível com **HACS (Custom Repo)**
- Serviço `edenred_pt.force_update` para forçar atualização de dados

## 📦 Instalação via HACS

1. Em **HACS → Custom repositories**, adicionar `https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt`
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
- `transaction_date`, `date`, `time`, `date_time`, `description`, `category`, `cat` _(abreviatura)_, `type` _(símbolo)_, `t` _(ícone colorido)_, `balance_after` e `movements` _(lista de movimentos, com (_`amount`_)_.

## 📜 Licença

MIT License
