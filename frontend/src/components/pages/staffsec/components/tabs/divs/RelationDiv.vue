<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Relation } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const RelationForm = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/forms/RelationForm.vue")
);

onBeforeMount( async() => {
  await props.getItem("staff");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Relation[],
    default: () => ({}),
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
});

const relation = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Relation>{},
});
</script>

<template>
  <h6>
    Связи
    <a
      class="btn btn-link"
      @click="
        relation.isForm = !relation.isForm;
        relation.action = relation.isForm ? 'create' : '';"
      :title="relation.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="relation.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="relation.isForm">
    <RelationForm
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :action="relation.action"
      :cand-id="candId"
      :content="relation.item"
      @deactivate="relation.isForm = false; relation.action = '';"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'relate' + idx"
        :idx="idx"
        :label="'Связь #' + (idx + 1)"
      >
      <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="props.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                relation.isForm = true;
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
</template>
