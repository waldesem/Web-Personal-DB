<script setup lang="ts">

const props = defineProps({
  store: {
    type: Object,
    required: true
  }
});

</script>


<template>
<div class="accordion" id="accordionRegistry" v-if="props.store.register?.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.register" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" 
              type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapseRegistry${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapseRegistry${tbl['id']}`" 
          :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
          data-bs-parent="#accordionRegistry">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" title="Удалить"
                  @click="props.store.deleteItem(tbl['id'].toString(), 'registry')">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>                    
                <a href="#" title="Изменить"
                  @click="props.store.openForm('registry', 'update', 
                                                  tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>    
          <tbody>
            <tr v-if="tbl['comments']">
              <td>Комментарий</td><td>{{ tbl['comments'] }}</td>
            </tr>
            <tr v-if="tbl['decision']">
              <td>Решение</td><td>{{ tbl['decision'] }}</td>
            </tr>
            <tr v-if="tbl['supervisor']">
              <td>Согласующий</td><td>{{ tbl['supervisor'] }}</td>
            </tr>
            <tr v-if="tbl['deadline']">
              <td>Дата</td><td>{{ new Date(tbl['deadline']).toLocaleDateString('ru-RU') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>