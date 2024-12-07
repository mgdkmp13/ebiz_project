{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}

<div class="images-container js-images-container">
  {block name='product_cover'}
    <div class="product-cover">
      {if $product.default_image}
        <!-- Powiększanie za pomocą FancyBox -->
        <a href="{$product.default_image.bySize.large_default.url}" data-fancybox="gallery" data-caption="{$product.default_image.legend|escape:'html'}">
          <img
            class="js-qv-product-cover img-fluid"
            src="{$product.default_image.bySize.large_default.url}"
            {if !empty($product.default_image.legend)}
              alt="{$product.default_image.legend|escape:'html'}"
              title="{$product.default_image.legend|escape:'html'}"
            {else}
              alt="{$product.name|escape:'html'}"
            {/if}
            loading="lazy"
            width="{$product.default_image.bySize.large_default.width}"
            height="{$product.default_image.bySize.large_default.height}"
          >
        </a>
      {else}
        <img
          class="img-fluid"
          src="{$urls.no_picture_image.bySize.medium_default.url}"
          alt="{l s='No image available' d='Shop.Theme.Catalog'}"
          loading="lazy"
          width="{$urls.no_picture_image.bySize.medium_default.width}"
          height="{$urls.no_picture_image.bySize.medium_default.height}"
        >
      {/if}
    </div>
  {/block}

  {block name='product_images'}
    <div class="js-qv-mask mask">
      <ul class="product-images js-qv-product-images">
        {foreach from=$product.images item=image}
          <li class="thumb-container js-thumb-container">
            <!-- Powiązanie miniatur z FancyBox -->
            <a href="{$image.bySize.large_default.url}" data-fancybox="gallery" data-caption="{$image.legend|escape:'html'}">
              <img
                class="thumb js-thumb {if $image.id_image == $product.default_image.id_image} selected js-thumb-selected {/if}"
                src="{$image.bySize.small_default.url}"
                {if !empty($image.legend)}
                  alt="{$image.legend|escape:'html'}"
                  title="{$image.legend|escape:'html'}"
                {else}
                  alt="{$product.name|escape:'html'}"
                {/if}
                loading="lazy"
                width="{$image.bySize.small_default.width}"
                height="{$image.bySize.small_default.height}"
              >
            </a>
          </li>
        {/foreach}
      </ul>
    </div>
  {/block}

  {hook h='displayAfterProductThumbs' product=$product}
</div>

{* Dodaj skrypt FancyBox i stylizację *}
{block name='javascript_head'}
  {include file="_partials/javascript.tpl" javascript=$javascript.head vars=$js_custom_vars}
  <script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/4.0.0/jquery.fancybox.min.js"></script>
{/block}

{block name='stylesheets'}
  {include file="_partials/stylesheets.tpl" stylesheets=$stylesheets}
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/4.0.0/jquery.fancybox.min.css">
{/block}
