<script setup lang="ts">
import { Button, FormControl } from 'frappe-ui'
import { ref } from 'vue'
import ChevronRight from '~icons/lucide/chevron-right'
import UploadIcon from '~icons/lucide/upload'

const brandName = ref('')
const logoUrl = ref(
	'https://github.com/user-attachments/assets/0a81cdc1-d957-47a9-b151-f5571be0d038'
)
const faviconUrl = ref('')
const enableForecasting = ref(false)

function removeLogo() {
	logoUrl.value = ''
}

function triggerFaviconUpload() {
	document.getElementById('favicon-input')?.click()
}

function onFaviconChange(e: Event) {
	const file = (e.target as HTMLInputElement).files?.[0]
	if (file) {
		faviconUrl.value = URL.createObjectURL(file)
	}
}
</script>

<template>
	<div class="mx-auto max-w-2xl px-10 py-8">
		<h1 class="mb-6 text-xl font-semibold text-ink-gray-9">General</h1>

		<!-- Branding -->
		<section class="mb-8">
			<h2 class="mb-4 text-p-base font-semibold text-ink-gray-9">Branding</h2>

			<div class="mb-5">
				<FormControl
					label="Brand name"
					v-model="brandName"
					type="text"
					placeholder="Enter brand name"
				/>
			</div>

			<!-- Logo -->
			<div
				class="mb-3 flex items-center gap-4 rounded-lg border border-outline-gray-2 px-4 py-3"
			>
				<div
					class="flex h-12 w-12 flex-shrink-0 items-center justify-center overflow-hidden rounded-md border border-outline-gray-2 bg-surface-gray-1"
				>
					<img
						v-if="logoUrl"
						:src="logoUrl"
						alt="Logo"
						class="h-full w-full object-contain"
					/>
					<span v-else class="text-p-xs text-ink-gray-4">—</span>
				</div>
				<div class="flex-1">
					<p class="text-p-sm font-medium text-ink-gray-9">Logo</p>
					<p class="text-p-xs text-ink-gray-5">
						Appears in the left sidebar. Recommended size is 32×32 px in PNG or SVG
					</p>
				</div>
				<Button variant="outline" @click="removeLogo">Remove</Button>
			</div>

			<!-- Favicon -->
			<div class="flex items-center gap-4 rounded-lg border border-outline-gray-2 px-4 py-3">
				<div
					class="flex h-12 w-12 flex-shrink-0 items-center justify-center overflow-hidden rounded-md border border-outline-gray-2 bg-surface-gray-1"
				>
					<img
						v-if="faviconUrl"
						:src="faviconUrl"
						alt="Favicon"
						class="h-full w-full object-contain"
					/>
					<svg
						v-else
						class="h-5 w-5 text-ink-gray-3"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="1.5"
					>
						<rect x="3" y="3" width="18" height="18" rx="2" />
						<path d="M3 9h18M9 21V9" />
					</svg>
				</div>
				<div class="flex-1">
					<p class="text-p-sm font-medium text-ink-gray-9">Favicon</p>
					<p class="text-p-xs text-ink-gray-5">
						Appears next to the title in your browser tab. Recommended size is 32×32 px
						in PNG or ICO
					</p>
				</div>
				<input
					id="favicon-input"
					type="file"
					accept="image/*"
					class="hidden"
					@change="onFaviconChange"
				/>
				<Button variant="outline" @click="triggerFaviconUpload">
					<template #prefix><UploadIcon class="h-3.5 w-3.5" /></template>
					Upload
				</Button>
			</div>
		</section>

		<hr class="mb-8 border-outline-gray-2" />

		<!-- Features & Preferences -->
		<section>
			<h2 class="mb-4 text-p-base font-semibold text-ink-gray-9">
				Features &amp; Preferences
			</h2>

			<div class="flex items-center justify-between border-b border-outline-gray-1 py-3.5">
				<div>
					<p class="text-p-sm font-medium text-ink-gray-9">Enable forecasting</p>
					<p class="text-p-xs text-ink-gray-5">
						Turn on predictive insights for your data.
					</p>
				</div>
				<FormControl type="checkbox" v-model="enableForecasting" />
			</div>

			<div class="flex items-center justify-between py-3.5">
				<div>
					<p class="text-p-sm font-medium text-ink-gray-9">
						Currency and exchange rate provider
					</p>
					<p class="text-p-xs text-ink-gray-5">
						Select currency display and data source.
					</p>
				</div>
				<Button variant="ghost">
					<template #suffix><ChevronRight class="h-4 w-4" /></template>
				</Button>
			</div>
		</section>
	</div>
</template>
