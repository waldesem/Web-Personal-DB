<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>

<template>
<div class="accordion" id="accordionAffilate" v-if="props.store.affilation.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.affilation" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseAffilate${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div class="accordion-collapse collapse" data-bs-parent="#accordionAffilate"
          :id="`collapseAffilate${tbl['id']}`" 
          :class="{ 'show': idx === 0}" >
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" @click="props.store.deleteItem('affilation', 'delete', tbl['id'].
                    toString())" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>
                <a class="btn btn-link" title="Изменить"
                  @click= "props.store.openForm('affilation', 'update', tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Тип участия</td><td>{{ tbl['view'] }}</td></tr>
            <tr><td>Организация</td><td>{{ tbl['name'] }}</td></tr>
            <tr><td>ИНН</td><td>{{ tbl['inn'] ? tbl['inn'] : 'Данных нет' }}</td></tr>
            <tr><td>Должность</td><td>{{ tbl['position'] }}</td></tr>
            <tr>
              <td>Дата декларации</td>
              <td>{{ new Date(tbl['deadline']).toLocaleDateString('ru-RU') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>