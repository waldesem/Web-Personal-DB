<script setup lang="ts">

const props = defineProps({
  store: {
  type: Object,
  required: true
  }
});

</script>


<template>
<div class="accordion" id="accordionInquiry" v-if="props.store.needs?.length" >
  <div class="accordion-item" v-for="tbl, idx in props.store.needs" :key="tbl['id']" >
    <h6 class="accordion-header">
      <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseInquiry${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseInquiry${tbl['id']}`" :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
        data-bs-parent="#accordionInquiry">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" title="Удалить"
                  @click="props.store.deleteItem(tbl['id'].toString(), 'inquiry')">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>                    
                <a href="#" title="Изменить"
                  @click="props.store.openForm('inquiry', 'update', 
                                                  tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>        
          <tbody>
            <tr>
              <td>Информация</td>
              <td>{{ tbl['info'] ? tbl['info'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Иннициатор</td>
              <td>{{ tbl['initiator'] ? tbl['initiator'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Источник</td>
              <td>{{ tbl['source'] ? tbl['source'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Сотрудник</td>
              <td>{{ tbl['officer'] ? tbl['officer'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Дата запроса</td>
              <td>{{ !tbl['deadline'] ? 'Данные отсутствуют'
                    : new Date(String(tbl['deadline'])).toLocaleDateString('ru-RU') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<p v-else >Данные отсутствуют</p>
</template>