<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>

<template>
<div class="accordion" id="accordionWork" v-if="props.store.works.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.works" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseWork${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseWork${tbl['id']}`" class="accordion-collapse collapse" 
          :class="{ 'show': idx === 0}" 
        data-bs-parent="#accordionWork">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" @click="props.store.deleteItem('workplace', 'delete', tbl['id'].
                    toString())" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>
                <a class="btn btn-link" title="Изменить"
                  @click= "props.store.openForm('workplace', 'update', tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Период</td>
              <td>{{ tbl['start_date'] }} - {{ tbl['end_date'] }}</td>
            </tr>
            <tr>
              <td>Организация</td>
              <td>{{ tbl['workplace'] ? tbl['workplace'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Адрес</td>
              <td>{{ tbl['address'] ? tbl['address'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Должность</td>
              <td>{{ tbl['position'] ? tbl['position'] : 'Данные отсутствуют' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>