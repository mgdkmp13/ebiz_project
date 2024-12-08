{assign var=_counter value=0}

{function name="menu" nodes=[] depth=0 parent=null}
    {if $nodes|count}
      <ul class="top-menu" {if $depth == 0}id="top-menu"{/if} data-depth="{$depth}">
        {foreach from=$nodes item=node key=node_key}
            <li class="{$node.type}{if $node.current} current{/if}" id="{$node.page_identifier}">
              <a
                class="{if $depth >= 0}dropdown-item{/if}{if $depth === 1} dropdown-submenu{/if}"
                href="{$node.url}" data-depth="{$depth}"
                {if $node.open_in_new_window} target="_blank" {/if}
              >
                <span>
                  {$node.label}
                  {if $depth == 0 && $node.children|count} <!-- Add arrow only for main categories -->
                    <i class="fas fa-chevron-down"></i> <!-- Arrow icon -->
                  {/if}
                </span>
                {if isset($node.image_urls) && $node.image_urls|@count > 0} <!-- Check if image_urls is an array and has elements -->
                  <div class="menu-image">
                    <img src="{$node.image_urls[0]}" alt="{$node.label}" class="menu-category-image"/>
                  </div>
                {/if}

                
              </a>

              {if $node.children|count}
                <div {if $depth === 0} class="popover sub-menu js-sub-menu collapse"{else} class="collapse"{/if} id="top_sub_menu_{$_counter}">
                  {menu nodes=$node.children depth=$node.depth parent=$node}
                </div>
              {/if}
            </li>

            {if $depth == 1 && $node_key != count($nodes)-1} <!-- Separator only for subcategories and not at the end -->
              <li class="dropdown-separator">
                <span>|</span>
              </li>
            {/if}

            {assign var=_counter value=$_counter+1} <!-- Increment counter for unique IDs -->
        {/foreach}
      </ul>
    {/if}
{/function}

<div class="menu js-top-menu position-static hidden-sm-down" id="_desktop_top_menu">
    {menu nodes=$menu.children}
    <div class="clearfix"></div>
</div>
