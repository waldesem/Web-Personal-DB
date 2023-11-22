<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  },
  hiddenDelBtn: Boolean,
  hiddeEditBtn: Boolean
});

</script>

<template>
  <div class="accordion" id="accordionCheck" v-if="props.store.verification?.length">
    <div class="accordion-item" v-for="tbl, idx in props.store.verification" 
                                :key="tbl['id']" >
      <h6 class="accordion-header">
        <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" type="button" data-bs-toggle="collapse" 
                :data-bs-target="`#collapseCheck${tbl['id']}`">
          {{ `ID #${tbl['id']}` }}
        </button>
      </h6>
      <div :id="`collapseCheck${tbl['id']}`" :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
          data-bs-parent="#accordionCheck">
        <div class="accordion-body">
          <table class="table table-responsive">
            <thead>
              <tr>
                <th width="25%">
                  <a :hidden="hiddenDelBtn" href="#" title="Удалить"
                    @click="props.store.deleteItem(tbl['id'].toString(), 'check')">
                    <i class="bi bi-trash"></i>
                  </a>
                </th>
                <th>                    
                  <a :hidden="hiddeEditBtn" href="#" title="Изменить"
                    @click="props.store.openForm('check', 'update', 
                                                    tbl['id'].toString(), tbl)">
                    <i class="bi bi-pencil-square"></i>
                  </a>
                </th>
              </tr>
            </thead>      
            <tbody>
              <tr>
                <td>Проверка по местам работы</td>
                <td>{{ tbl['workplace'] ? tbl['workplace'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Бывший работник МТСБ</td>
                <td>{{ tbl['employee'] ? tbl['employee'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка паспорта</td>
                <td>{{ tbl['document'] ? tbl['document'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка ИНН</td>
                <td>{{ tbl['inn'] ? tbl['inn'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка ФССП</td>
                <td>{{ tbl['debt'] ? tbl['debt'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка банкротства</td>
                <td>{{ tbl['bankruptcy'] ? tbl['bankruptcy'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка БКИ</td>
                <td>{{ tbl['bki'] ? tbl['bki'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка судебных дел</td>
                <td>{{ tbl['courts'] ? tbl['courts'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка аффилированности</td>
                <td>{{ tbl['affiliation'] ? tbl['affiliation'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка по списку террористов</td>
                <td>{{ tbl['terrorist'] ? tbl['terrorist'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка нахождения в розыске</td>
                <td>{{ tbl['mvd'] ? tbl['mvd'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка в открытых источниках</td>
                <td>{{ tbl['internet'] ? tbl['internet'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка Кронос</td>
                <td>{{ tbl['cronos'] ? tbl['cronos'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Проверка Крос</td>
                <td>{{ tbl['cros'] ? tbl['cros'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>Дополнительная информация</td>
                <td>{{ tbl['addition'] ? tbl['addition'] : 'Данные отсутствуют' }}</td>
              </tr>
              <tr>
                <td>ПФО</td>
                <td>{{ tbl['pfo'] ? "Назначено" : "Не назначено" }}</td>
              </tr>
              <tr v-if="tbl['comments']">
                <td>Комментарии</td>
                <td>{{ tbl['comments'] }}</td>
              </tr>
              <tr v-if="tbl['conclusion']">
                <td>Результат проверки</td>
                <td>{{ tbl['conclusion'] }}</td>
              </tr>
              <tr v-if="tbl['officer']">
                <td>Сотрудник</td>
                <td>
                  <a href="#" @click="props.store.getItem('check', 'self', tbl['id'].toString())">
                    {{ tbl['officer'] }}</a>
                </td>
              </tr>
              <tr v-if="tbl['deadline']">
                <td>Дата</td>
                <td>{{ new Date(String(tbl['deadline'])).toLocaleDateString('ru-RU') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  <p v-else >Данные отсутствуют</p>
</template>