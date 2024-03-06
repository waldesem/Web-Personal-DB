<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const RelationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/RelationForm.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get-item", "relation");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const relation = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit(){
  relation.value.action = '';
  relation.value.item = {};
};

function submitForm(form: Object) {
  emit("submit", [relation.value.action, "relation", relation.value.itemId, form])
  cancelEdit();
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "relation"])
};
</script>

<template>
  <h6>
    Связи
    <a
      class="btn btn-link"
      data-bs-toggle="modal"
      data-bs-target="#modalRelation"
      @click="
        relation.action = relation.action ? '' : 'create';"
        :title="relation.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="relation.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <ModalWin
    :title="
      relation.action === 'update' ? 'Изменить запись' : 'Добавить запись'
    "
    :id="'modalAddress'"
    @cancel="cancelEdit"
  >
    <RelationForm
      :content="relation.item"
      @submit="submitForm"
      @cancel="cancelEdit"
    />
  </ModalWin>
  <div v-if="props.items.length">
    <CollapseDiv
      v-for="(item, idx) in props.items"
      :key="idx"
      :id="'relate' + idx.toString()"
      :idx="idx.toString()"
      :label="'Связь #' + (idx + 1).toString()"
    >
      <RowDivSlot :slotTwo="true" :print="true">
        <template v-slot:divTwo>
          <a
            href="#"
            @click="deleteItem(item['id'].toString())"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            data-bs-toggle="modal"
            data-bs-target="#modalRelation"
            @click="
              relation.action = 'update';
              relation.item = item;
              relation.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </template>
      </RowDivSlot>
      <RowDivSlot :label="'Тип связи'" :value="item['relation']" />
      <RowDivSlot :label="'Связь'" :slotTwo="true">
        <router-link
          :to="{
            name: 'profile',
            params: { id: String(item['relation_id']) },
          }"
        >
          ID #{{ item["relation_id"] }}
        </router-link>
      </RowDivSlot>
    </CollapseDiv>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
