<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Contact } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const ContactForm = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/forms/ContactForm.vue")
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
    type: Array as () => Contact[],
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

const contact = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Contact>{},
});
</script>
</script>

<template>
  <h6>
    Контакты
    <a
      class="btn btn-link"
      @click="
        contact.isForm = !contact.isForm;
        contact.action = contact.isForm ? 'create' : '';"
      :title="contact.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="contact.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="contact.isForm">
    <ContactForm 
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :action="contact.action"
      :cand-id="candId"
      :content="contact.item"
      @deactivate="contact.isForm = false; contact.action = '';"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'cont' + idx"
        :idx="idx"
        :label="'Контакт #' + (idx + 1)"
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
                contact.isForm = true;
                contact.action = 'update';
                contact.item = item;
                contact.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Вид'" :value="item['view']" />
        <RowDivSlot :label="'Контакт'" :value="item['contact']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
