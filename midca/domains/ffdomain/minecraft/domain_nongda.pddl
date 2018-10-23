(define (domain minecraft-beta)
	(:requirements :typing :fluents :existential-preconditions)
	(:types
		resource - thing
		material - thing
		tool - thing
		craftgrid
		mapgrid
		direction
		player 
		monster - thing
		weapon - thing

		potion - thing
		helmet - thing
   	    chestplate - thing
	)



	(:predicates
		(player-at  ?loc - mapgrid)
		
		(in-shelter)
        (trap-destroyed ?loc - mapgrid)
        (searched-left ?obj - resource ?loc - mapgrid)
        (searched-right ?obj - resource ?loc - mapgrid)
        (searched-behind ?obj - resource ?loc - mapgrid)
        (searched-forward ?obj - resource ?loc - mapgrid)
        (looking-right  ?loc - mapgrid)
        (looking-left  ?loc - mapgrid)
        (looking-forward  ?loc - mapgrid)
        (looking-behind  ?loc - mapgrid)
		(thing-at-map  ?obj - resource  ?loc - mapgrid)
		(thing-at ?obj - resource ?loc - mapgrid)
		(known-loc ?obj - resource ?playerloc - mapgrid )
		(thing-at-loc ?obj - resource ?loc - mapgrid)
		(placed-thing-at-map  ?obj - material  ?loc - mapgrid)
		(resource-at-craft  ?res - thing  ?loc - craftgrid)
		(craft-empty  ?loc - craftgrid)
		(connect  ?from - mapgrid  ?to - mapgrid)
		(connect-left  ?from - mapgrid  ?to - mapgrid)
		(connect-right  ?from - mapgrid  ?to - mapgrid)
		(connect-behind  ?from - mapgrid  ?to - mapgrid)
		(connect-forward  ?from - mapgrid  ?to - mapgrid)
        (know-where ?res - resource ?loc - mapgrid)
		(crafting)
		(survive)
        (attacking ?loc - mapgrid)
		(looking-for ?res - resource ?loc - mapgrid)
		(head-armed)
   	    (chest-armed)
   	    (is-attacked ?loc - mapgrid)
   	    (is-trapped)
	)

	(:functions
		(thing-available  ?obj - thing)
		(current-harvest-duration)
		(current-harvest-location)
		(duration-need  ?tool - tool  ?res - resource)
		(location-id  ?loc - mapgrid)
		(tool-id  ?tool - tool)
		(tool-in-hand)
		(tool-max-health ?tool - tool)
		(tool-current-health ?tool - tool)
		(player-current-health)

		(current-hunger-value)

	)

	;;(:action restore-health
	;;	:parameters (?p -potion)
	;;	:precondition
	;;		(and
	;;;			(> (thing-available ?p) 0)
		;;		(< (player-current-health) 20)
	;;		)
	;;	:effect
	;;		(and
	;;			(assign (player-current-health) 20)
	;;			(decrease (thing-available ?p) 1)
	;;		)
	;;)


	;;-------------------------------------------------


	;; ----------------------------------------------------

	(:action place-on-map
		:parameters (?res - material  ?target - mapgrid)
		:precondition
			(and

				(player-at ?target)
				(not (placed-thing-at-map ?res ?target))
				(> (thing-available ?res) 0)

			)
		:effect
			(and
				(placed-thing-at-map ?res ?target)
				(decrease (thing-available ?res) 1)
				(assign (current-harvest-duration) 0)
			)
	)

	;; ----------------------------------------------------
	(:action move
		:parameters (?from - mapgrid ?to - mapgrid)
		:precondition
			(and
			 (> (player-current-health) 0)
				(player-at ?from)
				(connect ?from ?to)

			)
		:effect
			(and
				(player-at ?to)
				(not (player-at ?from))
				(assign (current-harvest-duration) 0)
				(assign (current-harvest-location) 0)
			)
	)
	;;----------------------------------------
	(:action find-forward
		:parameters (?res -resource ?playerloc - mapgrid )
		:precondition
			(and
			  ;; (chest-armed)
		    	;;(head-armed)
		    	(player-at ?playerloc)
				(not (known-loc ?res ?playerloc))
			)
		:effect
			(and
				(searched-forward ?res ?playerloc)
			    (looking-forward ?playerloc)
			)
	)
	;---------------------------------------------------------
	(:action find-left
		:parameters (?res -resource ?playerloc - mapgrid )
		:precondition
			(and
			    (searched-forward ?res ?playerloc)
			    (player-at ?playerloc)
				(not (known-loc ?res ?playerloc))
			)
		:effect
			(and
				(searched-left ?res ?playerloc)
				(not (looking-forward ?playerloc))
			    (looking-left ?playerloc)
			)
	)

    ;;----------------------------------------

	(:action find-right
		:parameters (?res -resource ?playerloc - mapgrid )
		:precondition
			(and
			    (searched-left ?res ?playerloc)
			    (player-at ?playerloc)
			    (not (known-loc ?res ?playerloc))
			)
		:effect
			(and
				(searched-right ?res ?playerloc)
				(not (looking-left ?playerloc))
				(looking-right ?playerloc)
			)
	)
	;;----------------------------------------

	(:action find-behind
		:parameters (?res -resource ?playerloc - mapgrid )
		:precondition
			(and
			   (searched-right ?res ?playerloc)
			   (player-at ?playerloc)
				(not (known-loc ?res ?playerloc))
			)
		:effect
			(and
				(known-loc ?res ?playerloc)
				(not (looking-right ?playerloc))
				(looking-behind ?playerloc)
				(looking-for ?res ?playerloc)
			)
	)



    ;;---------------------------
    ;;--------------------------------------------------------
	;;--------------------------------------------------------
	(:action attack-skeleton
		:parameters (?tool - tool ?loc - mapgrid)
		:precondition
			(and
			(> (player-current-health) 0)
			    (player-at ?loc)
				(known-loc skeleton ?loc)
				(thing-at skeleton ?loc)
				(= (tool-id ?tool) 10)
				(= (tool-in-hand) 10)


			)
		:effect
			(and

				(not (thing-at skeleton ?loc))
				(attacking ?loc)
			)
	)

	;;----------------------------------
    (:action destroy-trap-with-loc
		:parameters (?tool - tool ?loc - mapgrid ?player_loc - mapgrid)
		:precondition
			(and
			(> (player-current-health) 0)
				(thing-at-map arrowtrap ?loc)
				;;(thing-at arrowtrap ?player_loc)
				(= (tool-id ?tool) 11)
				(= (tool-in-hand) 11)
                (player-at ?player_loc)
			)
		:effect
			(and

				(not (thing-at-map arrowtrap ?loc))
			(trap-destroyed ?player_loc)
			)
	)
;;

(:action attack-skeleton-with-loc
		:parameters (?tool - tool ?loc - mapgrid ?player_loc - mapgrid)
		:precondition
			(and
			(> (player-current-health) 0)
				(thing-at-map skeleton ?loc)

				(= (tool-id ?tool) 10)
				(= (tool-in-hand) 10)
                (player-at ?player_loc)
			)
		:effect
			(and

				(not (thing-at-map skeleton ?loc))
			(attacking ?player_loc)
			)
	)

	;;--------------------------------------------------------
	(:action destroy-trap
		:parameters (?tool - tool ?loc - mapgrid)
		:precondition
			(and
			(> (player-current-health) 0)
			    (player-at ?loc)
				(known-loc arrowtrap ?loc)
				(thing-at arrowtrap ?loc)
				(= (tool-id ?tool) 11)
				(= (tool-in-hand) 11)

			)
		:effect
			(and
				(not (thing-at arrowtrap ?loc))
				(trap-destroyed ?loc)
			)
	)
	;------------------------------------------------------------


	(:action change-harvest-loc
		:parameters (?target - mapgrid)
		:precondition
			(and
				(not (= (current-harvest-location) (location-id ?target)))
				(player-at ?target)

			)
		:effect
			(and
				;;(assign (current-harvest-duration) 0)
				(assign (current-harvest-location) (location-id ?target))
			)
	)

	;; ----------------------------------------------------
	(:action change-harvest-tool
		:parameters (?tool - tool)
		:precondition
			(and
				(not (= (tool-in-hand) (tool-id ?tool)))
				(> (thing-available ?tool) 0)

			)
		:effect
			(and 
				(assign (current-harvest-duration) 0)
				(assign (tool-in-hand) (tool-id ?tool))
			)
	)
	;;-----------------------------------------------
	
	(:action move-to-shelter
		:parameters (?target - mapgrid )
		:precondition
			(and
				(player-at ?target)
				(thing-at-map shelter ?target)
				(not (in-shelter))
				
			)
		:effect
			(and
				(in-shelter)
			)
	)
	;;----------------------------------------------------
	(:action wear-chestplate
		:parameters (?chestplate - chestplate )
		:precondition
			(and
				(> (thing-available ?chestplate) 0)

			)
		:effect
			(and
				(chest-armed)
			)
	)
    ;;---------------------------------------------------
    (:action wear-helmet
		:parameters (?helmet - helmet )
		:precondition
			(and
				(> (thing-available ?helmet) 0)

			)
		:effect
			(and
				(head-armed)
			)
	)

	;; ----------------------------------------------------
	(:action harvest
		:parameters (?target - mapgrid ?tool - tool ?obj - resource)
		:precondition
			(and
				(player-at ?target)
				(> (thing-available ?tool) 0)
				(thing-at-map ?obj ?target)
				(= (current-harvest-location) (location-id ?target))
				(= (tool-in-hand) (tool-id ?tool))


			)
		:effect
			(and
				(increase (current-harvest-duration) 1)
				(decrease (tool-current-health ?tool) 1)
			)
	)

	;; ----------------------------------------------------
	(:action harvest-loose-tool
		:parameters (?tool - tool)
		:precondition
			(and
				(> (thing-available ?tool) 0)
				(= (tool-in-hand) (tool-id ?tool))
				(= (tool-current-health ?tool) 0)

			)
		:effect
			(and
				(decrease (thing-available ?tool) 1)
				(assign (tool-current-health ?tool) (tool-max-health ?tool))
			)
	)

	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;; Harvesting
	;;  tree -> wood
	;;	rock -> stone
	;;	coalore -> coal
	;;	ironore -> ironore
	;;	tallgrass -> seeds
	;;	wheatgrass -> wheat
	;;	sandrock -> sandstone
	;;	soil -> sand
	;;	claysoil -> clay
	;;	brown-mushroom -> brown-mushroom
	;;	red-mushroom -> red-mushroom
	;;	skeleton -> bone
	;;	sugarcane -> sugar
	;;	cobweb : shears -> 1 string
	;;	chicken : hand -> egg
	;;	water : fishingrod -> fish
	;;	sheep : shears -> 4 wool
	;;	cow : bucket -> milk

	;; ----------------------------------------------------
	(:action get-harvest-wood
		:parameters (?target - mapgrid ?tool - tool)
		:precondition
			(and
			(> (player-current-health) 0)
				(player-at ?target)
				(thing-at-map tree ?target)
				(= (tool-in-hand) (tool-id ?tool))
				(= (current-harvest-location) (location-id ?target))


			)
		:effect
			(and
				(increase (thing-available wood) 1)
				(not (thing-at-map tree ?target))
			)
	)


)