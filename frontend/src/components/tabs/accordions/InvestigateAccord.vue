<script setup lang="ts">

const props = defineProps({
  store: {
  type: Object,
  required: true
  }
});

</script>


<template>
<div class="accordion" id="accordionInvestigation" v-if="props.store.inquisition?.length" >
  <div class="accordion-item" v-for="tbl, idx in props.store.inquisition" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseInvestigation{tbl['id']}`">
        {{ `ID #{tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseInvestigation{tbl['id']}`" class="accordion-collapse collapse" :class="{ 'show': idx === 0}" 
        data-bs-parent="#accordionInvestigation">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" title="Удалить"
                  @click="props.store.deleteItem(tbl['id'].toString(), 'investigation')">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>                    
                <a href="#" title="Изменить"
                  @click="props.store.openForm('investigation', 'update', 
                                                  tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>        
          <tbody>
            <tr>
              <td>Тема</td>
              <td>{{ tbl['theme'] ? tbl['theme'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Информация</td>
              <td>{{ tbl['info'] ? tbl['info'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Сотрудник</td>
              <td>{{ tbl['officer'] ? tbl['officer'] : 'Данные отсутствуют' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>