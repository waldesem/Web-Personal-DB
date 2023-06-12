<template>
  <NavbarView />
  <div class="container py-5">
    <AlertMessage v-if="attr" :attr="attr" :text="text" />
    <div class="py-3">
      <h5>{{ fullname }}</h5>
    </div>  
    <div class="nav nav-tabs nav-justified" role="tablist">
      <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#anketaTab" type="button" role="tab">Анкета</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#checkTab" type="button" role="tab">Проверки</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#registryTab" type="button" role="tab">Согласования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#poligrafTab" type="button" role="tab">Полиграф</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#investigationTab" type="button" role="tab">Расследования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#inquiryTab" type="button" role="tab">Запросы</button>
    </div>
    <div class="tab-content">
      <div class="tab-pane active py-1" role="tabpanel" id="anketaTab">
        <AnketaView :table="anketa" :candId="candId" :resume="resume" :status="status" :state="state" @updateMessage="returnChild" @updateItem="getProfile"/>
      </div>
      <div class="tab-pane py-1" role="tabpanel" id="checkTab">
        <CheckView :table="check" :candId="candId" :item="lastCheck" :status="status" :state="state" @updateMessage="returnChild" @updateItem="getProfile" />
      </div>
      <div class="tab-pane py-1" role="tabpanel" id="registryTab">
        <RegistryView :table="registry" :candId="candId" @updateMessage="returnChild" @updateItem="getProfile" />
      </div>
      <div class="tab-pane py-1" role="tabpanel" id="poligrafTab">
        <PoligrafView :table="poligraf" :candId="candId" @updateMessage="returnChild" @updateItem="getProfile" />
      </div>
      <div class="tab-pane py-1" role="tabpanel" id="investigationTab">
        <InvestigationView :table="investigation" :candId="candId" @updateMessage="returnChild" @updateItem="getProfile" />
      </div>
      <div class="tab-pane py-1" role="tabpanel" id="inquiryTab">
        <InquiryView :table="inquiry" :candId="candId" @updateMessage="returnChild" @updateItem="getProfile" />
      </div>
    </div>
  </div>
</template>

<script>
import NavbarView from './Navbar.vue';
import AlertMessage from './Message.vue';
import AnketaView from './profile/AnketaTab.vue';
import CheckView from './profile/CheckTab.vue';
import RegistryView from './profile/RegistryTab.vue';
import PoligrafView from './profile/PoligrafTab.vue';
import InvestigationView from './profile/InvestigateTab.vue';
import InquiryView from './profile/InquiryTab.vue';

export default {
  name: 'ProfileApp',
  
  components: {
    NavbarView,
    AlertMessage,
    AnketaView,
    CheckView,
    RegistryView,
    PoligrafView,
    InvestigationView,
    InquiryView
  },

  data() {
    return {
      attr: '',
      text: '',
      candId: '', 
      anketa: '',
      resume: {},
      check: '',
      lastCheck: {},
      registry: '', 
      poligraf: '', 
      investigation: '', 
      inquiry: '', 
      status: '',
      state: {},
      fullname: '',
      anketa_divs: ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа'],
      anketa_labels: [
        ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 
        'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Статус', 'Дата', 'Рекрутер', 'Внешний id'],
        ['Должность', 'Департамент'],
        ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
        ['Тип', 'Регион', 'Адрес'],
        ['Вид', 'Контакт'],
        ['Период', 'Организация', 'Адрес', 'Должность'],
        ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'],
      ],
      check_labels: [
        'ID', 'Статус автопроверки', 'Проверка по местам работы', 'Бывший работник МТСБ', 
        'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ', 
        'Проверка судебных дел', 'Проверка аффилированности', 'Проверка в списке террористов', 
        'Проверка нахождения в розыске', 'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 
        'Дополнительная информация', 'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки', 
        'Дата проверки', 'Сотрудник СБ'
      ],
      registry_labels: ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий'],
      poligraf_labels: ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'],
      investigation_labels: ['ID', 'Тематика', 'Информация', 'Дата проверки'],
      inquiry_labels: ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса']
    }
  },

  methods: {

    returnChild (data){
      this.attr = data["attr"];
      this.text = data["text"];
    },

    async getProfile(candId = this.candId) {
      const response = await fetch(`http://localhost:5000/profile/${candId}`, {
      headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`}
      });
      const [anketa, check, registry, poligraf, investigation, inquiry, state] = await response.json();
      this.anketa = this.anketa_divs.map((div, i) => `
        <div class="py-1"><h6>${div}</h6>${this.createItemTable(this.anketa_labels[i], anketa[i])}</div>
        `).join('');
      this.fullname = anketa[0][0]['fullname'];
      this.status = anketa[0][0]['status'];
      this.state = state;
      this.resume = anketa[0][0];
      this.lastCheck = check[0];
      this.check = this.createItemTable(this.check_labels, check);
      this.registry = this.createItemTable(this.registry_labels, registry);
      this.poligraf = this.createItemTable(this.poligraf_labels, poligraf);
      this.investigation = this.createItemTable(this.investigation_labels, investigation);
      this.inquiry = this.createItemTable(this.inquiry_labels, inquiry)
    },

    createItemTable(names, response) {
      if (!response.length) {
        return `<p>Данные отсутствуют</p>`
      }
      const rows = response.map((item) => {
        return names.map((name, i) => {
          if (Object.keys(item)[i] === 'deadline' || Object.keys(item)[i] === 'birthday') {
            const date = new Date(Object.values(item)[i]);
            return `<tr><td width="25%">${name}</td><td>${date.toLocaleDateString('ru-RU')}</td></tr>`;
          } else if (Object.keys(item)[i] === 'id' ) {
            return `<tr height="50px"><th colspan="2">${name} #${Object.values(item)[i]}</th></tr>`;
          } else if (Object.keys(item)[i] === 'path' ) {
            return `<tr><td width="25%">${name}</td><td><a href="${Object.values(item)[i]}">Открыть</a></td></tr>`;
          } else {
            return `<tr><td width="25%">${name}</td><td>${Object.values(item)[i]}</td></tr>`;
          }
        }).join('');
      });
      const body = `<tbody>${rows.join('')}</tbody>`;
      return `<table class="table table-responsive">${body}</table>`
      }
    },
  
  async created() {
    const candId = this.$route.params.id;
    this.candId = candId;
    this.getProfile()
  }
}
</script>
