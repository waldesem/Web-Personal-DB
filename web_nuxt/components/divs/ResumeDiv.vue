<script setup lang="ts">
import type { Persons } from "@/types";
import { emitMessage } from "@/utils";

const emit = defineEmits(["update"]);

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const status = inject("status") as Ref<string>;
const person = inject("person") as Ref<Persons>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const resume = ref({} as Persons);

async function submitResume(form: Persons) {
  pending.value = true;
  modal.value = false;
  const { message } = (await authFetch('/route/items/persons', {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  resume.value = {} as Persons;
  emit("update");
  emitMessage(message);
}

async function deleteItem() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/persons/${candId.value}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  emitMessage(message);
  return navigateTo("/persons");
}
</script>

<template>
  <ElementsCardDiv>
    <UModal v-model="modal" prevent-close>
      <ElementsCardDiv>
        <FormsResumeForm
          :resume="resume"
          @update="submitResume"
          @cancel="
            resume = {} as Persons;
            modal = false;
          "
        />
      </ElementsCardDiv>
    </UModal>
    <div v-if="pending || status === 'pending'">
      <div v-for="i in 14" :key="i" class="flex grid grid-cols-12 gap-3 mb-3">
        <div class="col-span-3">
          <USkeleton class="h-4" />
        </div>
        <div class="col-span-9">
          <USkeleton class="h-4 w-[300px]" />
        </div>
      </div>
    </div>
    <div v-else>
      <ElementsLabelSlot :label="'Фамилия'">
        {{ person.surname }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Имя'">
        {{ person.firstname }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Отчество'">
        {{ person.patronymic }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата рождения'">
        {{ new Date(person.birthday).toLocaleDateString("ru-RU") }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Место рождения'">
        {{ person.birthplace }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Гражданство'">
        {{ person.citizenship }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="person.dual" :label="'Двойное гражданство'">
        {{ person.dual }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'СНИЛС'">
        {{ person.snils }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'ИНН'">
        {{ person.inn }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Семейное положение'">
        {{ person.marital }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата записи'">
        {{ new Date(person.created).toLocaleString("ru-RU") }}
      </ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="person.addition"
        :label="'Дополнительная информация'"
      >
        {{ person.addition }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Материалы'">
        {{ person.destination }}
      </ElementsLabelSlot>
    </div>
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'persons'"
        @delete="deleteItem"
        @update="
          resume = person;
          modal = true;
        "
      />
    </template>
  </ElementsCardDiv>
</template>
