<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInit1a59eaf9a9b10bb694b6ee72716c7d9a
{
    public static $classMap = array (
        'Ps_Emailsubscription' => __DIR__ . '/../..' . '/ps_emailsubscription.php',
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->classMap = ComposerStaticInit1a59eaf9a9b10bb694b6ee72716c7d9a::$classMap;

        }, null, ClassLoader::class);
    }
}
