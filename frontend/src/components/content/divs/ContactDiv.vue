<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Contact } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const ContactForm = defineAsyncComponent(
  () => import("@components/content/forms/ContactForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(async () => {
  emit("get-item", "contact");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Contact>,
    default: {},
  },
});

const contact = ref({
  action: "",
  itemId: "",
  item: <Contact>{},
});

function submitForm(form: Object) {
  emit("submit", contact.value.action, "contact", contact.value.itemId, form);
  contact.value.action = "";
};
</script>

<template>
  <ActionHeader
    :header="'Контакты'"
    :action="contact.action"
    @action="contact.action = contact.action ? '' : 'create'"
  />
  <ContactForm v-if="contact.action"
    :contact="contact.item" 
    @submit="submitForm" 
    @cancel="contact.action = ''"
  />
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'cont' + idx"
        :idx="idx.toString()"
        :label="'Контакт #' + (idx + 1)"
      >
        <LabelSlot :label="'Действия'" :no-print="true">
          <ActionIcons
            @delete="emit('delete', item['id'].toString(), 'contact')"
            @update="
              contact.action = 'update';
              contact.item = item;
              contact.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item['id'] }}</LabelSlot>
        <LabelSlot :label="'Вид'">{{ item['view'] }}</LabelSlot>
        <LabelSlot :label="'Контакт'">{{ item['contact'] }}</LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
