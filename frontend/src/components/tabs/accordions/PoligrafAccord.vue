<script setup lang="ts">

const props = defineProps({
  store: {
  type: Object,
  required: true
  }
});

</script>


<template>
<div class="accordion" id="accordionPoligraf" v-if="props.store.pfo?.length">
  <div class="accordion-item" v-for="tbl, idx in props.store.pfo" 
                              :key="tbl['id']" >
    <h6 class="accordion-header">
      <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" type="button" data-bs-toggle="collapse" 
              :data-bs-target="`#collapsePoligraf${tbl['id']}`">
        {{ `ID #${tbl['id']}` }}
      </button>
    </h6>
    <div :id="`collapsePoligraf${tbl['id']}`" :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
        data-bs-parent="#accordionPoligraf">
      <div class="accordion-body">
        <table class="table table-responsive">
          <thead>
            <tr>
              <th width="25%">
                <a href="#" title="Удалить"
                  @click="props.store.deleteItem(tbl['id'].toString(), 'poligraf')">
                  <i class="bi bi-trash"></i>
                </a>
              </th>
              <th>                    
                <a href="#" title="Изменить"
                  @click="props.store.openForm('poligraf', 'update', 
                                                  tbl['id'].toString(), tbl)">
                  <i class="bi bi-pencil-square"></i>
                </a>
              </th>
            </tr>
          </thead>        
          <tbody>
            <tr>
              <td>Тема</td>
              <td>{{ tbl['theme'] ? tbl['theme'] : 'Данные отсуствуют' }}</td>
            </tr>
            <tr>
              <td>Результат</td>
              <td>{{ tbl['results'] ? tbl['results'] : 'Данные отсуствуют' }}</td>
            </tr>
            <tr v-if="tbl['path']">
              <td>Ссылка</td>
              <td>
                <router-link :to="{ name: 'manager',  params: { group: 'staffsec', path: tbl['path'].split('/') } }">
                  {{ props.store.resume['path'] }}
                </router-link>
              </td>
            </tr>
            <tr>
              <td>Полиграфолог</td>
              <td>{{ tbl['officer'] ? tbl['officer'] : 'Данные отсуствуют' }}</td>
            </tr>
            <tr>
              <td>Дата</td>
              <td>{{ tbl['deadline'] ? new Date(String(tbl['deadline'])).
                toLocaleDateString('ru-RU') : 'Данные отсуствуют' }}</td>
            </tr>
            <tr>
              <td colspan="2">
                <form class="form" enctype="multipart/form-data" role="form" 
                      @change="props.store.submitFile($event, 'poligraf', tbl['id'].toString())">
                  <input class="form-control" id="file" type="file" ref="file" multiple>
                </form>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<p v-else >Данные отсутствуют</p>
</template>