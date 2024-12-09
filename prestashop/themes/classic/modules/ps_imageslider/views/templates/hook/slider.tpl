{assign var="myArray" value=["https://localhost:8443/order/10624-stormcast-christmas-jumper-aos.html", "https://localhost:8443/394-gifts", "https://localhost:8443/393-2025-calendars"]}

{if $homeslider.slides}
  <div class="info">
    <a href=".">
      <h2>INFORMACJE O DOSTAWIE!</h2>
    </a>
  </div>
  <div class="info2">
    <a href=".">
      <h2>NOWE ZESTAWY PREZENTOWE JUŻ DOSTĘPNE!</h2>
    </a>
  </div>

  <!-- Pierwsza instancja slidera -->
  <div id="carousel-1" data-ride="carousel" class="carousel slide" data-interval="{$homeslider.speed}" data-wrap="{(string)$homeslider.wrap}" data-pause="{$homeslider.pause}" data-touch="true">
    <ol class="carousel-indicators">
      {foreach from=$homeslider.slides item=slide key=idxSlide name='homeslider'}
        <li data-target="#carousel-1" data-slide-to="{$idxSlide}"{if $idxSlide == 0} class="active"{/if}></li>
      {/foreach}
    </ol>
    <ul class="carousel-inner" role="listbox" aria-label="{l s='Carousel container' d='Shop.Theme.Global'}">
      {foreach from=$homeslider.slides item=slide key=idxSlide name='homeslider'}
        {if isset($myArray[$idxSlide])}
          {assign var="currentUrl" value=$myArray[$idxSlide]}
        {else}
          {assign var="currentUrl" value="#"}
        {/if}
        <li class="carousel-item {if $smarty.foreach.homeslider.first}active{/if}" role="option" aria-hidden="{if $smarty.foreach.homeslider.first}false{else}true{/if}">
          <a href="{$currentUrl}">
            <figure>
              <img src="{$slide.image_url}" alt="{$slide.legend|escape}" loading="lazy" width="1110" height="340">
              {if $slide.title || $slide.description}
                <figcaption class="caption">
                  <h2 class="display-1 text-uppercase">{$slide.title}</h2>
                  <div class="caption-description">{$slide.description nofilter}</div>
                </figcaption>
              {/if}
            </figure>
          </a>
        </li>
      {/foreach}
    </ul>
    <div class="direction" aria-label="{l s='Carousel buttons' d='Shop.Theme.Global'}">
      <a class="left carousel-control" href="#carousel-1" role="button" data-slide="prev" aria-label="{l s='Previous' d='Shop.Theme.Global'}">
        <span class="icon-prev hidden-xs" aria-hidden="true">
          <i class="material-icons">&#xE5CB;</i>
        </span>
      </a>
      <a class="right carousel-control" href="#carousel-1" role="button" data-slide="next" aria-label="{l s='Next' d='Shop.Theme.Global'}">
        <span class="icon-next" aria-hidden="true">
          <i class="material-icons">&#xE5CC;</i>
        </span>
      </a>
    </div>
  </div>

  {assign var=imgUrl value=["https://localhost:8443/modules/ps_imageslider/images/slide2_1.webp", 
                            "https://localhost:8443/modules/ps_imageslider/images/slide2_2.webp", 
                            "https://localhost:8443/modules/ps_imageslider/images/slide2_3.webp"]}

{assign var=imgUrl value=["https://localhost:8443/modules/ps_imageslider/images/slide2_1.webp", 
                            "https://localhost:8443/modules/ps_imageslider/images/slide2_2.webp", 
                            "https://localhost:8443/modules/ps_imageslider/images/slide2_3.webp"]}

<!-- Druga instancja slidera -->
<div id="carousel-2" data-ride="carousel" class="carousel slide" data-interval="{$homeslider.speed}" data-wrap="{(string)$homeslider.wrap}" data-pause="{$homeslider.pause}" data-touch="true">
  <ol class="carousel-indicators">
    {foreach from=$imgUrl item=image key=idxImage}
      <li data-target="#carousel-2" data-slide-to="{$idxImage}" {if $idxImage == 0} class="active" {/if}></li>
    {/foreach}
  </ol>
  <ul class="carousel-inner" role="listbox" aria-label="{l s='Carousel container' d='Shop.Theme.Global'}">
    {foreach from=$imgUrl item=image key=idxImage}
      <li class="carousel-item {if $idxImage == 0}active{/if}" role="option" aria-hidden="{if $idxImage == 0}false{else}true{/if}">
        <a href="#">
          <figure>
            <img src="{$image}" alt="Slide {$idxImage+1}" loading="lazy" width="1110" height="340">
          </figure>
        </a>
      </li>
    {/foreach}
  </ul>
  <div class="direction" aria-label="{l s='Carousel buttons' d='Shop.Theme.Global'}">
    <a class="left carousel-control" href="#carousel-2" role="button" data-slide="prev" aria-label="{l s='Previous' d='Shop.Theme.Global'}">
      <span class="icon-prev hidden-xs" aria-hidden="true">
        <i class="material-icons">&#xE5CB;</i>
      </span>
    </a>
    <a class="right carousel-control" href="#carousel-2" role="button" data-slide="next" aria-label="{l s='Next' d='Shop.Theme.Global'}">
      <span class="icon-next" aria-hidden="true">
        <i class="material-icons">&#xE5CC;</i>
      </span>
    </a>
  </div>
</div>


{/if}
