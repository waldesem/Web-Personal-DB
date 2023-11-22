<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>

<template>
<div class="accordion" id="accordionDocument" v-if="props.store.docums.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.docums" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseDocument${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseDocument${tbl['id']}`" class="accordion-collapse collapse" 
          :class="{ 'show': idx === 0}" 
        data-bs-parent="#accordionDocument">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" @click="props.store.deleteItem('document', 'delete', tbl['id'].
                    toString())" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>
                <a class="btn btn-link" title="Изменить"
                  @click= "props.store.openForm('document', 'update', tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Вид документа</td>
              <td>{{ tbl['view'] ? tbl['view'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Серия</td>
              <td>{{ tbl['series'] ? tbl['series'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Номер</td>
              <td>{{ tbl['number'] ? tbl['number'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Кем выдан</td>
              <td>{{ tbl['agency'] ? tbl['agency'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Дата выдачи</td>
              <td>{{ tbl['issue'] ? new Date(String(tbl['issue'])).toLocaleDateString('ru-RU') 
                                  : 'Данные отсутствуют' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>